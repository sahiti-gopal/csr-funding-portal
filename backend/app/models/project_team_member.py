from app.extensions import db
from app.models.base import BaseModel


class ProjectTeamMember(BaseModel):
    __tablename__ = "project_team_members"

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
    )

    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150))
    tag = db.Column(db.String(50))

    project = db.relationship(
        "Project",
        backref=db.backref(
            "team_members",
            cascade="all, delete-orphan",
            order_by="ProjectTeamMember.id",
        ),
    )

    def __repr__(self):
        return f"<ProjectTeamMember {self.name}>"
