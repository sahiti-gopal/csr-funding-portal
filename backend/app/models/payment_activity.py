from app.extensions import db


class PaymentActivity(db.Model):
    __tablename__ = "payment_activity"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id")
    )

    title = db.Column(
        db.String(255)
    )

    activity_type = db.Column(
        db.String(100)
    )

    activity_date = db.Column(
        db.DateTime
    )

    def icon(self):
        mapping = {
            "PAYMENT_RECEIVED": "bank",
            "DOCUMENT_UPLOADED": "upload",
            "DOCUMENT_VERIFIED": "verified",
            "FUND_ALLOCATED": "allocation",
            "PAYMENT_PENDING": "clock",
            "PAYMENT_OVERDUE": "alert",
            "AI_INSIGHT": "sparkles",
        }

        return mapping.get(
            self.activity_type,
            "activity"
        )