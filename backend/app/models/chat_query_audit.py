from app.extensions import db
from app.models.base import BaseModel


class ChatQueryAudit(BaseModel):
    __tablename__ = "chat_query_audits"

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=False,
        index=True,
    )
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    question_text = db.Column(db.Text, nullable=False)
    normalized_question = db.Column(db.String(500), nullable=False, index=True)

    # fast_path | cache | llm | fallback | error
    response_source = db.Column(db.String(20), nullable=False)

    sql_generated = db.Column(db.Text, nullable=True)
    sql_attempt_count = db.Column(db.Integer, default=1)

    gemini_model = db.Column(db.String(64), nullable=True)
    sql_gen_latency_ms = db.Column(db.Integer, nullable=True)
    narrative_gen_latency_ms = db.Column(db.Integer, nullable=True)
    total_latency_ms = db.Column(db.Integer, nullable=False)

    row_count = db.Column(db.Integer, nullable=True)
    cache_hit = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.Text, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)

    prompt_tokens = db.Column(db.Integer, nullable=True)
    completion_tokens = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<ChatQueryAudit message={self.message_id} source={self.response_source}>"
