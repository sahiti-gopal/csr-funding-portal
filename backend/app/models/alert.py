from app.extensions import db
from app.models.base import BaseModel


class Alert(BaseModel):
    __tablename__ = "alerts"

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)

    category = db.Column(db.String(50), nullable=False)

    priority = db.Column(
        db.String(20),
        default="LOW"
    )

    status = db.Column(
        db.String(20),
        default="Unread"
    )

    due_date = db.Column(db.Date)

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    is_resolved = db.Column(
        db.Boolean,
        default=False
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=True
    )

    project = db.relationship(
        "Project",
        backref="alerts"
    )