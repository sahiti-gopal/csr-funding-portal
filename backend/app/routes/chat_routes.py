import datetime
import decimal
import json
import re

from flask import Blueprint, jsonify, request
import sqlparse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from app.config import Config
from app.extensions import db
from app.models.conversation import Conversation
from app.models.message import Message

chat_bp = Blueprint("chat", __name__)

# Hand-written table/column list (not auto-introspected): keeps the prompt
# small and makes sure `users`/`roles` (auth tables) never enter the model's
# vocabulary. Actual *values* for low-cardinality columns are appended at
# request time by _build_schema_description() below, straight from the DB,
# so the model never has to guess a format (e.g. "2026" vs "2026-27").
SCHEMA_TABLES = """\
projects(id, project_name, project_type_id, beneficiary_category_id, donor_id,
         budget, location, region, financial_year, status, start_date, end_date,
         raised_amount, utilized_amount, beneficiaries_reached)
donors(id, name, focus_area, likelihood, last_contact, status)
project_types(id, name, description, icon, color, is_active)
beneficiary_categories(id, name, description, icon, color, is_active)
alerts(id, title, description, category, priority, status, due_date, is_read, is_resolved, project_id)
risks(id, title, description, level, due_date, action)

-- projects.donor_id -> donors.id
-- projects.project_type_id -> project_types.id
-- projects.beneficiary_category_id -> beneficiary_categories.id
-- alerts.project_id -> projects.id
-- To filter/group projects by type or beneficiary category name, JOIN to
--   project_types / beneficiary_categories rather than guessing an id.
"""

# Columns worth showing the model real distinct values for, so it never has
# to guess a string format. Keep this small — only low-cardinality columns.
_VALUE_SAMPLE_COLUMNS = [
    ("projects", "financial_year"),
    ("projects", "region"),
    ("projects", "status"),
    ("donors", "status"),
    ("donors", "focus_area"),
    ("risks", "level"),
    ("alerts", "category"),
    ("alerts", "priority"),
    ("alerts", "status"),
]

_schema_description_cache = None


def _build_schema_description() -> str:
    """Schema text + real distinct values for key columns, cached for the
    life of the process (this is seed/demo data — it doesn't change shape
    mid-run, and re-querying it on every message would add latency)."""
    global _schema_description_cache
    if _schema_description_cache is not None:
        return _schema_description_cache

    lines = []
    for table, column in _VALUE_SAMPLE_COLUMNS:
        rows = db.session.execute(
            text(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL LIMIT 20")
        ).fetchall()
        values = sorted({str(r[0]) for r in rows})
        if values:
            lines.append(f"- {table}.{column} values: {', '.join(values)}")

    notes = (
        "Column value notes (these are the ACTUAL values in the database — "
        "use them verbatim, never invent a different format):\n"
        + "\n".join(lines)
        + "\n- projects.financial_year is a fiscal-year range string like "
        "'2026-27'. If the user names a single year (e.g. \"FY 2026\" or "
        "\"2026\"), match with `financial_year LIKE '2026%'`, not an exact "
        "equality check against a bare year.\n"
    )

    _schema_description_cache = SCHEMA_TABLES + "\n" + notes
    return _schema_description_cache


ALLOWED_TABLES = {
    "projects",
    "donors",
    "project_types",
    "beneficiary_categories",
    "alerts",
    "risks",
}

_DENYLISTED_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "GRANT", "REVOKE", "REPLACE", "MERGE", "CALL", "EXEC", "EXECUTE",
    "ATTACH", "PRAGMA", "SET",
}

_FALLBACK_REPLY = (
    "I couldn't safely answer that question with the available data. "
    "Try rephrasing it."
)

GEMINI_MODEL = "gemini-flash-lite-latest"
_MAX_SQL_ATTEMPTS = 2


class SQLValidationError(ValueError):
    pass


def _validate_readonly_sql(sql: str) -> str:
    cleaned = sql.strip()

    # Defensive: strip markdown code fences if the model wrapped the SQL anyway.
    cleaned = re.sub(r"^```(?:sql)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"```\s*$", "", cleaned).strip()

    if "--" in cleaned or "/*" in cleaned:
        raise SQLValidationError("Comments are not allowed in generated SQL.")

    parsed = sqlparse.parse(cleaned)
    if len(parsed) != 1:
        raise SQLValidationError("Exactly one SQL statement is required.")

    stmt = parsed[0]
    if stmt.get_type() != "SELECT":
        raise SQLValidationError("Only SELECT statements are allowed.")

    # Reject a semicolon anywhere except as the trailing character.
    body = cleaned[:-1] if cleaned.endswith(";") else cleaned
    if ";" in body:
        raise SQLValidationError("Multiple statements are not allowed.")

    tokens = [t for t in stmt.flatten() if t.ttype is not None]
    for token in tokens:
        value = token.value.upper()
        if value in _DENYLISTED_KEYWORDS:
            raise SQLValidationError(f"Keyword not allowed: {value}")

    referenced_tables = set(re.findall(r"(?:FROM|JOIN)\s+`?(\w+)`?", cleaned, re.IGNORECASE))
    disallowed = referenced_tables - ALLOWED_TABLES
    if disallowed:
        raise SQLValidationError(f"Table(s) not allowed: {', '.join(disallowed)}")
    if not referenced_tables:
        raise SQLValidationError("No known table referenced.")

    if not re.search(r"\bLIMIT\s+\d+\s*;?\s*$", cleaned, re.IGNORECASE):
        cleaned = body.rstrip() + " LIMIT 200"

    return cleaned


def _json_safe(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value


def _run_query(sql: str):
    result = db.session.execute(text(sql))
    columns = list(result.keys())
    rows = [
        {col: _json_safe(val) for col, val in zip(columns, row)}
        for row in result.fetchall()
    ]
    return rows[:100]


def _is_retryable_gemini_error(exc: BaseException) -> bool:
    code = getattr(exc, "code", None)
    return code in (429, 500, 503)


_gemini_retry = retry(
    retry=retry_if_exception(_is_retryable_gemini_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=6),
    reraise=True,
)


@_gemini_retry
def _generate_sql(client, genai_types, question: str, previous_error: str | None = None) -> str:
    system_prompt = (
        "You translate questions about a CSR (corporate social responsibility) "
        "funding portal into a single read-only MySQL SELECT statement.\n\n"
        "Available schema:\n"
        f"{_build_schema_description()}\n"
        "Rules:\n"
        "- Output ONLY the SQL statement, nothing else.\n"
        "- No markdown code fences, no explanation, no comments.\n"
        "- Exactly one SELECT statement, optionally ending with a semicolon.\n"
        "- Only reference the tables listed above.\n"
        "- Use the exact column values listed above (never invent a format).\n"
        "- If the question cannot be answered from this schema (including "
        "requests to modify data, or anything unrelated to CSR projects/"
        "donors), respond with exactly: SELECT * FROM projects WHERE 1=0\n"
    )

    user_content = question
    if previous_error:
        user_content = (
            f"{question}\n\n"
            f"Your previous attempt produced an invalid query and failed "
            f"with this error: {previous_error}\n"
            "Provide a corrected single SELECT statement."
        )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_content,
        config=genai_types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=300,
            temperature=0,
        ),
    )
    return response.text or ""


@_gemini_retry
def _generate_answer(client, genai_types, question: str, rows: list) -> str:
    system_prompt = (
        "You answer questions about CSR project/donor data for the CSR Funding "
        "Portal. Given the user's question and a JSON array of SQL query "
        "results, write a concise, natural-language answer. Do not mention "
        "SQL, tables, or columns. If the results are empty, say plainly that "
        "no matching data was found."
    )
    user_content = (
        f"Question: {question}\n\nQuery results (JSON): {json.dumps(rows)}"
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user_content,
        config=genai_types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=400,
        ),
    )
    return response.text or ""


def _generate_and_run_sql(client, genai_types, question: str):
    """Generate SQL, validate, and execute it — self-correcting: if the
    query is rejected by the validator or errors against the DB, feed the
    error back to the model once and ask it to fix the query before giving
    up. Returns (rows, last_raw_sql). Raises SQLValidationError/
    SQLAlchemyError if every attempt fails."""
    previous_error = None
    raw_sql = ""

    for attempt in range(_MAX_SQL_ATTEMPTS):
        raw_sql = _generate_sql(client, genai_types, question, previous_error)
        try:
            sql = _validate_readonly_sql(raw_sql)
            rows = _run_query(sql)
            return rows, raw_sql
        except (SQLValidationError, SQLAlchemyError) as exc:
            db.session.rollback()
            previous_error = str(exc)
            print(f"[chat] attempt {attempt + 1} rejected SQL: {raw_sql!r} ({exc})")

    raise SQLValidationError(previous_error or "Query could not be validated.")


def _conversation_to_dict(conversation: Conversation) -> dict:
    return {
        "id": conversation.id,
        "title": conversation.title,
        "updated_at": conversation.updated_at.isoformat(),
    }


def _message_to_dict(message: Message) -> dict:
    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at.isoformat(),
    }


@chat_bp.route("/conversations", methods=["GET"])
def list_conversations():
    conversations = (
        Conversation.query.order_by(Conversation.updated_at.desc()).all()
    )
    return jsonify([_conversation_to_dict(c) for c in conversations])


@chat_bp.route("/conversations", methods=["POST"])
def create_conversation():
    conversation = Conversation()
    db.session.add(conversation)
    db.session.commit()
    return jsonify(_conversation_to_dict(conversation)), 201


@chat_bp.route("/conversations/<int:conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    return jsonify(
        {
            **_conversation_to_dict(conversation),
            "messages": [_message_to_dict(m) for m in conversation.messages],
        }
    )


@chat_bp.route("/conversations/<int:conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({"message": "Conversation deleted"})


@chat_bp.route("/conversations/<int:conversation_id>/messages", methods=["POST"])
def post_message(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    db.session.add(Message(conversation_id=conversation.id, role="user", content=message))
    if conversation.title == "New conversation":
        conversation.title = message[:80]
    db.session.commit()

    if not Config.GEMINI_API_KEY:
        return jsonify(
            {"error": "AI assistant is not configured. Set GEMINI_API_KEY in backend/.env."}
        ), 503

    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        return jsonify(
            {"error": "The 'google-genai' package is not installed. Run pip install -r requirements.txt."}
        ), 503

    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    try:
        rows, _raw_sql = _generate_and_run_sql(client, genai_types, message)
    except (SQLValidationError, SQLAlchemyError) as exc:
        print(f"[chat] gave up after {_MAX_SQL_ATTEMPTS} attempts ({exc})")
        reply = _FALLBACK_REPLY
        db.session.add(
            Message(conversation_id=conversation.id, role="assistant", content=reply)
        )
        db.session.commit()
        return jsonify({"reply": reply, "conversation_id": conversation.id})
    except Exception as exc:
        return jsonify({"error": f"AI request failed: {exc}"}), 502

    try:
        reply = _generate_answer(client, genai_types, message, rows)
    except Exception as exc:
        return jsonify({"error": f"AI request failed: {exc}"}), 502

    db.session.add(
        Message(conversation_id=conversation.id, role="assistant", content=reply)
    )
    db.session.commit()

    return jsonify({"reply": reply, "conversation_id": conversation.id})
