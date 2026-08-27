"""Chat pipeline orchestrator — glues every stage together in the exact
order of the target architecture:

  Preprocessor (intent+entities)
      -> [fast path: skips straight past cache/LLM]
      -> Cache check (no LLM)
      -> Confidence scorer (question+entities)
      -> SQL generator (schema only)   -- only reached on the "llm" route
      -> SQL verifier (checks syntax/scope)
      -> SQL executor (runs against the DB)
      -> PRIVACY BOUNDARY:
           real rows  -> returned directly for the UI's results table
           row_count + columns only -> Result formatter (no data param)
      -> Answer to user (narrative + real table), never crossing the
         boundary back the other way.
"""

import re
import time

from sqlalchemy.exc import SQLAlchemyError

_AGGREGATE_COLUMN_PATTERN = re.compile(r"^(count|sum|avg|min|max)\(", re.IGNORECASE)


def _extract_aggregate_values(rows: list, columns: list) -> dict | None:
    """A single row with aggregate-looking column names (COUNT(*), SUM(x), ...)
    is a computed statistic, not a raw record — safe to let cross the privacy
    boundary into the narrative, unlike individual row values."""
    if len(rows) != 1:
        return None
    aggregate_columns = [c for c in columns if _AGGREGATE_COLUMN_PATTERN.match(c)]
    if not aggregate_columns:
        return None
    return {c: rows[0][c] for c in aggregate_columns}

from app.config import Config
from app.extensions import db
from app.models.chat_failed_question import ChatFailedQuestion
from app.models.chat_query_audit import ChatQueryAudit
from app.services.chat import cache as cache_stage
from app.services.chat.confidence import decide_route
from app.services.chat.history import get_recent_history
from app.services.chat.preprocessor import preprocess
from app.services.chat.result_formatter import generate_answer
from app.services.chat.sql_pipeline import (
    SQLValidationError,
    generate_and_run_sql,
    run_query,
    validate_readonly_sql,
)

FALLBACK_REPLY = (
    "I couldn't safely answer that question with the available data. "
    "Try rephrasing it."
)


def handle_chat_message(conversation, message_row, question: str) -> dict:
    """Returns {"reply": str, "table": {"columns": [...], "rows": [...]} | None,
    "meta": {"source": str, "cached": bool, "row_count": int | None}}."""
    started = time.monotonic()

    # ---- Stage 1: Preprocessor (intent + entities) ----
    preprocessed = preprocess(question)

    if not Config.GEMINI_API_KEY:
        raise RuntimeError("AI assistant is not configured. Set GEMINI_API_KEY in backend/.env.")
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        raise RuntimeError("The 'google-genai' package is not installed. Run pip install -r requirements.txt.")

    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    # ---- Stage 2: Cache check (skipped entirely on a fast-path match) ----
    cached_sql = None
    if preprocessed.fast_path_rule is None:
        cached_sql = cache_stage.get_cached_sql(preprocessed.normalized)

    # ---- Stage 3: Confidence scorer ----
    route = decide_route(preprocessed, cached_sql)

    sql_gen_started = time.monotonic()
    attempt_count = 1
    narrative_gen_latency_ms = None

    try:
        if route.source in ("fast_path", "cache"):
            sql = validate_readonly_sql(route.sql)
            rows = run_query(sql)
        else:
            # ---- Stage 4/5/6: SQL generator -> verifier -> executor ----
            # `route.entities` (from the confidence scorer) is forwarded as a
            # hint to the SQL generator's prompt — the diagram's
            # "confidence scorer (question+entities) -> SQL generator" arrow.
            # `conversation_history` (last 10 messages) resolves pronouns/
            # follow-ups; `last_sql` lets a pure filter-tweak reuse the prior
            # query's structure instead of rederiving it from scratch.
            history = get_recent_history(conversation.id, exclude_message_id=message_row.id)
            rows, sql, attempt_count = generate_and_run_sql(
                client, genai_types, question, route.entities,
                history, conversation.last_generated_sql,
            )
            cache_stage.store_cached_sql(preprocessed.normalized, sql)
    except (SQLValidationError, SQLAlchemyError) as exc:
        db.session.rollback()
        print(f"[chat] gave up after retries ({exc})")
        _record_failure(conversation, message_row, question, failure_stage="sql_validation", error=str(exc))
        _record_audit(
            message_row, conversation, question, preprocessed.normalized,
            response_source="fallback", sql_generated=None, sql_attempt_count=attempt_count,
            sql_gen_latency_ms=_elapsed_ms(sql_gen_started), narrative_gen_latency_ms=None,
            total_latency_ms=_elapsed_ms(started), row_count=None, cache_hit=False,
            error_message=str(exc), confidence_score=route.entity_confidence,
        )
        return {
            "reply": FALLBACK_REPLY,
            "table": None,
            "meta": {"source": "fallback", "cached": False, "row_count": None, "confidence": route.entity_confidence, "entities": route.entities},
        }
    except Exception as exc:
        _record_failure(conversation, message_row, question, failure_stage="gemini_error", error=str(exc))
        raise
    sql_gen_latency_ms = _elapsed_ms(sql_gen_started)

    conversation.last_generated_sql = sql
    db.session.commit()

    columns = list(rows[0].keys()) if rows else []

    # ---- PRIVACY BOUNDARY ----
    # `rows` (real values) go straight into the response for the UI table.
    # The result formatter below receives only row_count/columns — never `rows`.
    if route.source == "fast_path":
        # Skips the LLM entirely, including the narrative — that's the point
        # of a fast path. A fixed template is enough since the shape of the
        # answer is already known.
        reply = f"Here are the {len(rows)} results."
    else:
        narrative_started = time.monotonic()
        aggregate_values = _extract_aggregate_values(rows, columns)
        try:
            reply = generate_answer(client, genai_types, question, len(rows), columns, aggregate_values)
        except Exception as exc:
            _record_failure(conversation, message_row, question, failure_stage="gemini_error", error=str(exc), last_sql=sql)
            raise
        narrative_gen_latency_ms = _elapsed_ms(narrative_started)

    _record_audit(
        message_row, conversation, question, preprocessed.normalized,
        response_source=route.source, sql_generated=sql, sql_attempt_count=attempt_count,
        sql_gen_latency_ms=sql_gen_latency_ms, narrative_gen_latency_ms=narrative_gen_latency_ms,
        total_latency_ms=_elapsed_ms(started), row_count=len(rows), cache_hit=(route.source == "cache"),
        error_message=None, confidence_score=route.entity_confidence,
    )

    return {
        "reply": reply,
        "table": {"columns": columns, "rows": rows} if rows else None,
        "sql": sql,
        "meta": {
            "source": route.source,
            "cached": route.source == "cache",
            "row_count": len(rows),
            "confidence": route.entity_confidence,
            "entities": route.entities,
        },
    }


def _elapsed_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _record_audit(message_row, conversation, question, normalized, **fields):
    audit = ChatQueryAudit(
        message_id=message_row.id,
        conversation_id=conversation.id,
        question_text=question,
        normalized_question=normalized,
        gemini_model="gemini-flash-lite-latest",
        **fields,
    )
    db.session.add(audit)
    db.session.commit()


def _record_failure(conversation, message_row, question, *, failure_stage, error, last_sql=None):
    db.session.add(
        ChatFailedQuestion(
            message_id=message_row.id if message_row else None,
            conversation_id=conversation.id if conversation else None,
            question_text=question,
            failure_stage=failure_stage,
            last_error=error,
            last_sql_attempted=last_sql,
            attempt_count=1,
        )
    )
    db.session.commit()
