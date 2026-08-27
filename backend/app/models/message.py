from app.extensions import db
from app.models.base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False,
    )

    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)

    sql_generated = db.Column(db.Text, nullable=True)
    table_data = db.Column(db.JSON, nullable=True)
    # fast_path | cache | llm | fallback | error
    response_source = db.Column(db.String(20), nullable=True)
    # up | down | null (no feedback given)
    feedback = db.Column(db.String(10), nullable=True)

    conversation = db.relationship(
        "Conversation",
        backref=db.backref(
            "messages",
            cascade="all, delete-orphan",
            order_by="Message.id",
        ),
    )

    def __repr__(self):
        return f"<Message {self.role}:{self.id}>"
