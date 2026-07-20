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
