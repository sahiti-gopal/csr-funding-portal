from app.extensions import db
from app.models.base import BaseModel


class ProjectDocument(BaseModel):
    __tablename__ = "project_documents"

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
    )

    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(50))

    project = db.relationship(
        "Project",
        backref=db.backref(
            "documents",
            cascade="all, delete-orphan",
            order_by="ProjectDocument.id",
        ),
    )

    def __repr__(self):
        return f"<ProjectDocument {self.name}>"
