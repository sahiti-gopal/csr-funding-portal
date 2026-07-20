from app.extensions import db
from app.models.base import BaseModel


class Conversation(BaseModel):
    __tablename__ = "conversations"

    title = db.Column(db.String(200), nullable=False, default="New conversation")

    def __repr__(self):
        return f"<Conversation {self.title}>"
