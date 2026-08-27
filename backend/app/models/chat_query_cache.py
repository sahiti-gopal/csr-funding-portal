from app.extensions import db
from app.models.base import BaseModel


class ChatQueryCache(BaseModel):
    __tablename__ = "chat_query_cache"

    question_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)
    normalized_question = db.Column(db.String(500), nullable=False)
    sql_text = db.Column(db.Text, nullable=False)

    hit_count = db.Column(db.Integer, default=0)
    last_hit_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)

    def __repr__(self):
        return f"<ChatQueryCache {self.question_hash[:8]}>"
