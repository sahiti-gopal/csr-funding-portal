from app.extensions import db
from app.models.base import BaseModel


class Report(BaseModel):
    __tablename__ = "reports"
    __table_args__ = (
        db.UniqueConstraint("donor_id", "financial_year", name="uq_report_donor_fy"),
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=False,
    )

    financial_year = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Pending review | Approved | Failed
    review_status = db.Column(db.String(30), nullable=False, default="Pending review")

    # Awaiting | Delivered
    delivery_status = db.Column(db.String(30), nullable=False, default="Awaiting")

    generated_at = db.Column(db.DateTime)
    content = db.Column(db.JSON)
    error_message = db.Column(db.Text)

    donor = db.relationship("Donor", backref="reports")

    def __repr__(self):
        return f"<Report {self.title}>"
