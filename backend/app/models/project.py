from app.extensions import db
from app.models.base import BaseModel


class Project(BaseModel):
    __tablename__ = "projects"

    project_name = db.Column(db.String(200), nullable=False)

    project_type_id = db.Column(
        db.Integer,
        db.ForeignKey("project_types.id"),
        nullable=False,
    )

    beneficiary_category_id = db.Column(
        db.Integer,
        db.ForeignKey("beneficiary_categories.id"),
        nullable=False,
    )

    budget = db.Column(db.Float, nullable=False)

    location = db.Column(db.String(150))

    # NEW
    region = db.Column(db.String(50))

    # NEW
    financial_year = db.Column(db.String(20))

    status = db.Column(db.String(50), default="Planning")

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=True,
    )

    # Dashboard fields
    raised_amount = db.Column(db.Float, default=0)

    utilized_amount = db.Column(db.Float, default=0)

    beneficiaries_reached = db.Column(db.Integer, default=0)

    project_type = db.relationship(
        "ProjectType",
        backref="projects"
    )

    beneficiary_category = db.relationship(
        "BeneficiaryCategory",
        backref="projects"
    )

    donor = db.relationship(
        "Donor",
        backref="projects"
    )

    def __repr__(self):
        return f"<Project {self.project_name}>"