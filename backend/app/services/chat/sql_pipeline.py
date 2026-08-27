import datetime
import decimal
import re

import sqlparse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from app.extensions import db
from app.services.chat.schema import ALLOWED_TABLES, build_schema_description

GEMINI_MODEL = "gemini-flash-lite-latest"
MAX_SQL_ATTEMPTS = 2

_DENYLISTED_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "GRANT", "REVOKE", "REPLACE", "MERGE", "CALL", "EXEC", "EXECUTE",
    "ATTACH", "PRAGMA", "SET",
}


class SQLValidationError(ValueError):
    pass


def validate_readonly_sql(sql: str) -> str:
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

    referenced_tables = extract_referenced_tables(cleaned)
    disallowed = referenced_tables - ALLOWED_TABLES
    if disallowed:
        raise SQLValidationError(f"Table(s) not allowed: {', '.join(disallowed)}")
    if not referenced_tables:
        raise SQLValidationError("No known table referenced.")

    if not re.search(r"\bLIMIT\s+\d+\s*;?\s*$", cleaned, re.IGNORECASE):
        cleaned = body.rstrip() + " LIMIT 200"

    return cleaned


def extract_referenced_tables(sql: str) -> set:
    """Shared by the validator and the eval harness so they can't drift apart."""
    return set(re.findall(r"(?:FROM|JOIN)\s+`?(\w+)`?", sql, re.IGNORECASE))


def json_safe(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    return value


def run_query(sql: str):
    result = db.session.execute(text(sql))
    columns = list(result.keys())
    rows = [
        {col: json_safe(val) for col, val in zip(columns, row)}
        for row in result.fetchall()
    ]
    return rows[:100]


MAX_FEW_SHOT_EXAMPLES = 5


def build_few_shot_block() -> str:
    """Loads the most recently thumbs-up-promoted question->SQL pairs as
    few-shot examples. Re-validates each one before use — a promoted
    example is still an outside input (a user's approval, not a guarantee),
    so it goes through the same guardrail as every other SQL source rather
    than being trusted just because it ran successfully once before."""
    from app.models.chat_promoted_example import ChatPromotedExample

    examples = (
        ChatPromotedExample.query.order_by(ChatPromotedExample.created_at.desc())
        .limit(MAX_FEW_SHOT_EXAMPLES)
        .all()
    )
    valid_examples = []
    for example in examples:
        try:
            validate_readonly_sql(example.sql_text)
        except SQLValidationError:
            continue
        valid_examples.append(example)

    if not valid_examples:
        return ""

    lines = ["\nExamples of previously confirmed-correct question -> SQL pairs:"]
    for example in valid_examples:
        lines.append(f"Q: {example.question_text}\nSQL: {example.sql_text}")
    return "\n".join(lines) + "\n"


def _is_retryable_gemini_error(exc: BaseException) -> bool:
    code = getattr(exc, "code", None)
    return code in (429, 500, 503)


gemini_retry = retry(
    retry=retry_if_exception(_is_retryable_gemini_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=6),
    reraise=True,
)


@gemini_retry
def generate_sql(
    client, genai_types, question: str,
    previous_error: str | None = None, entities: dict | None = None,
    conversation_history: list | None = None, last_sql: str | None = None,
) -> str:
    system_prompt = (
        "You translate questions about a CSR (corporate social responsibility) "
        "funding portal into a single read-only MySQL SELECT statement.\n\n"
        "Available schema:\n"
        f"{build_schema_description()}\n"
        "Rules:\n"
        "- Output ONLY the SQL statement, nothing else.\n"
        "- No markdown code fences, no explanation, no comments.\n"
        "- Exactly one SELECT statement, optionally ending with a semicolon.\n"
        "- Only reference the tables listed above.\n"
        "- Use the exact column values listed above (never invent a format).\n"
        "- If a 'Detected entities' hint is given below, treat it as a strong "
        "signal for which WHERE-clause filters the question likely needs — "
        "but still read the question itself for the actual intent.\n"
        "- If 'Most recent SQL in this conversation' is given below and the "
        "current question only tweaks a filter (e.g. \"now just the North "
        "region\", \"what about last year\"), reuse that SQL's structure and "
        "adjust only what the question changes — don't rederive it from "
        "scratch.\n"
        "- If the question cannot be answered from this schema (including "
        "requests to modify data, or anything unrelated to CSR projects/"
        "donors), respond with exactly: SELECT * FROM projects WHERE 1=0\n"
        f"{build_few_shot_block()}"
    )

    user_content = question
    if conversation_history:
        thread = "\n".join(f"{m['role']}: {m['content']}" for m in conversation_history)
        user_content = f"Conversation so far:\n{thread}\n\nCurrent question: {question}"
    if last_sql:
        user_content += f"\n\nMost recent SQL in this conversation: {last_sql}"
    if entities:
        hint = ", ".join(f"{key}={value}" for key, value in entities.items())
        user_content += f"\n\nDetected entities: {hint}"
    if previous_error:
        user_content = (
            f"{user_content}\n\n"
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


def generate_and_run_sql(
    client, genai_types, question: str, entities: dict | None = None,
    conversation_history: list | None = None, last_sql: str | None = None,
):
    """Generate SQL, validate, and execute it — self-correcting: if the
    query is rejected by the validator or errors against the DB, feed the
    error back to the model once and ask it to fix the query before giving
    up. Returns (rows, last_raw_sql, attempt_count). Raises
    SQLValidationError/SQLAlchemyError if every attempt fails."""
    previous_error = None
    raw_sql = ""

    for attempt in range(MAX_SQL_ATTEMPTS):
        raw_sql = generate_sql(
            client, genai_types, question, previous_error, entities,
            conversation_history, last_sql,
        )
        try:
            sql = validate_readonly_sql(raw_sql)
            rows = run_query(sql)
            return rows, sql, attempt + 1
        except (SQLValidationError, SQLAlchemyError) as exc:
            db.session.rollback()
            previous_error = str(exc)
            print(f"[chat] attempt {attempt + 1} rejected SQL: {raw_sql!r} ({exc})")

    raise SQLValidationError(previous_error or "Query could not be validated.")
