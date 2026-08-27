from app.extensions import db
from app.models.base import BaseModel


class Conversation(BaseModel):
    __tablename__ = "conversations"

    title = db.Column(db.String(200), nullable=False, default="New conversation")

    # Most recently generated SQL in this conversation — lets a pure
    # filter-only follow-up ("now just the North region") reuse/adapt it
    # instead of re-deriving the query from scratch. Distinct from the
    # global exact-match ChatQueryCache, which is keyed by question text
    # across all conversations, not scoped to "what came right before this."
    last_generated_sql = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Conversation {self.title}>"
