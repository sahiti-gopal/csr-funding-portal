from app.extensions import db
from app.models.base import BaseModel


class ProjectLocation(BaseModel):
    __tablename__ = "project_locations"

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
    )

    name = db.Column(db.String(120), nullable=False)

    project = db.relationship(
        "Project",
        backref=db.backref(
            "locations",
            cascade="all, delete-orphan",
            order_by="ProjectLocation.id",
        ),
    )

    def __repr__(self):
        return f"<ProjectLocation {self.name}>"
