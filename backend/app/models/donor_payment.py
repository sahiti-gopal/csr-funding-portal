from app.extensions import db


class DonorPayment(db.Model):
    __tablename__ = "donor_payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=False
    )

    installment_name = db.Column(
        db.String(100),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(14, 2),
        nullable=False
    )

    due_date = db.Column(
        db.Date
    )

    received_date = db.Column(
        db.Date
    )

    payment_mode = db.Column(
        db.String(50)
    )

    transaction_id = db.Column(
        db.String(150)
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    remarks = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    documents = db.relationship(
        "PaymentDocument",
        backref="payment",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "donor_id": self.donor_id,
            "installment": self.installment_name,
            "amount": float(self.amount),
            "due_date": self.due_date.isoformat()
            if self.due_date else None,
            "received_date": self.received_date.isoformat()
            if self.received_date else None,
            "payment_mode": self.payment_mode,
            "transaction_id": self.transaction_id,
            "status": self.status,
            "remarks": self.remarks
        }