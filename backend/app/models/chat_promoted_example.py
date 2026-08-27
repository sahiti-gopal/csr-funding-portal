from app.extensions import db
from app.models.base import BaseModel


class ChatPromotedExample(BaseModel):
    """A question -> SQL pair promoted into the few-shot prompt after a
    user thumbs-up on an llm-sourced answer. Databricks Genie calls this
    "promoting a good Q&A to a curated example" — same idea, minus the
    admin curation UI. Re-validated at promotion time (not just trusted
    because it ran once) so a bad answer can't poison future prompts."""

    __tablename__ = "chat_promoted_examples"

    question_text = db.Column(db.Text, nullable=False)
    sql_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ChatPromotedExample {self.question_text[:40]!r}>"
