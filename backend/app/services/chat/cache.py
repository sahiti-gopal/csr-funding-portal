"""Cache-check stage — DB-backed (no redis; MySQL is the only store shared
across gunicorn workers). Caches SQL text only, never row data: results are
always re-executed live, so only the LLM round-trip is skipped on a hit."""

import hashlib
import random
from datetime import datetime, timedelta

from app.extensions import db
from app.models.chat_query_cache import ChatQueryCache

CACHE_TTL_HOURS = 6


def _hash_question(normalized_question: str) -> str:
    return hashlib.sha256(normalized_question.encode("utf-8")).hexdigest()


def get_cached_sql(normalized_question: str) -> str | None:
    question_hash = _hash_question(normalized_question)
    entry = ChatQueryCache.query.filter_by(question_hash=question_hash).first()
    if entry is None or entry.expires_at < datetime.utcnow():
        return None

    entry.hit_count += 1
    entry.last_hit_at = datetime.utcnow()
    db.session.commit()
    return entry.sql_text


def store_cached_sql(normalized_question: str, sql_text: str) -> None:
    question_hash = _hash_question(normalized_question)
    entry = ChatQueryCache.query.filter_by(question_hash=question_hash).first()
    expires_at = datetime.utcnow() + timedelta(hours=CACHE_TTL_HOURS)

    if entry is None:
        db.session.add(
            ChatQueryCache(
                question_hash=question_hash,
                normalized_question=normalized_question,
                sql_text=sql_text,
                expires_at=expires_at,
            )
        )
    else:
        entry.sql_text = sql_text
        entry.expires_at = expires_at

    if random.random() < 0.01:
        ChatQueryCache.query.filter(ChatQueryCache.expires_at < datetime.utcnow()).delete()

    db.session.commit()
