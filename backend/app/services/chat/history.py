"""Conversation-history stage — hard-capped at the last 10 messages, no
summarization. Enough thread context for the LLM to resolve pronouns/
follow-ups without letting the prompt grow unbounded as a conversation
gets long."""

from app.models.message import Message

HISTORY_LIMIT = 10


def get_recent_history(conversation_id: int, exclude_message_id: int | None = None) -> list:
    """Returns up to the last HISTORY_LIMIT messages for this conversation,
    oldest first, as [{"role": ..., "content": ...}, ...]."""
    query = Message.query.filter(Message.conversation_id == conversation_id)
    if exclude_message_id is not None:
        query = query.filter(Message.id != exclude_message_id)

    recent = (
        query.order_by(Message.id.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )
    recent.reverse()
    return [{"role": m.role, "content": m.content} for m in recent]
