from app.extensions import db
from app.models.base import BaseModel


class ChatFailedQuestion(BaseModel):
    __tablename__ = "chat_failed_questions"

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=True,
        index=True,
    )
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=True,
        index=True,
    )

    question_text = db.Column(db.Text, nullable=False)

    # sql_generation | sql_validation | sql_execution | gemini_error | rate_limited
    failure_stage = db.Column(db.String(30), nullable=False)

    last_error = db.Column(db.Text, nullable=True)
    last_sql_attempted = db.Column(db.Text, nullable=True)
    attempt_count = db.Column(db.Integer, default=1)

    resolved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<ChatFailedQuestion {self.failure_stage} resolved={self.resolved}>"
