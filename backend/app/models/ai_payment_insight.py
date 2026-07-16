from app.extensions import db


class AIPaymentInsight(db.Model):
    __tablename__ = "ai_payment_insights"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=True
    )

    title = db.Column(
        db.String(255),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.String(20),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def priority_color(self):
        colors = {
            "High": "#EF4444",
            "Medium": "#F59E0B",
            "Low": "#22C55E",
        }
        return colors.get(self.priority, "#2563EB")

    def to_dict(self):
        return {
            "id": self.id,
            "donor_id": self.donor_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "priorityColor": self.priority_color(),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }