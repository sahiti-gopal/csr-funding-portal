from app.extensions import db
from app.models.base import BaseModel


class Risk(BaseModel):
    __tablename__ = "risks"

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))

    # High | Medium | Low
    level = db.Column(db.String(30), default="Medium")

    due_date = db.Column(db.Date)
    action = db.Column(db.String(150))

    # icon key: file | check | shield
    icon = db.Column(db.String(30), default="file")

    def __repr__(self):
        return f"<Risk {self.title}>"
