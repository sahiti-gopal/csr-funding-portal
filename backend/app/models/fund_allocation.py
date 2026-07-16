from app.extensions import db


class FundAllocation(db.Model):
    __tablename__ = "fund_allocations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id")
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id")
    )

    allocated_amount = db.Column(
        db.Numeric(14, 2)
    )

    utilized_amount = db.Column(
        db.Numeric(14, 2)
    )

    remaining_amount = db.Column(
        db.Numeric(14, 2)
    )

    allocation_date = db.Column(
        db.Date
    )

    project = db.relationship(
        "Project",
        lazy=True
    )

    def utilization_percent(self):
        allocated = float(self.allocated_amount or 0)

        if allocated == 0:
            return 0

        utilized = float(self.utilized_amount or 0)

        return round(
            utilized / allocated * 100,
            1
        )