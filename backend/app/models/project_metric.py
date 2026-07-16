from app.extensions import db
from app.models.base import BaseModel


class ProjectMetric(BaseModel):
    __tablename__ = "project_metrics"

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
    )

    icon = db.Column(db.String(50))
    title = db.Column(db.String(150), nullable=False)
    current_value = db.Column(db.Integer, default=0)
    target_value = db.Column(db.Integer, default=0)

    project = db.relationship(
        "Project",
        backref=db.backref(
            "metrics",
            cascade="all, delete-orphan",
            order_by="ProjectMetric.id",
        ),
    )

    def __repr__(self):
        return f"<ProjectMetric {self.title}>"
