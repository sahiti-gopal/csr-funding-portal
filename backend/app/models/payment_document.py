from app.extensions import db


class PaymentDocument(db.Model):
    __tablename__ = "payment_documents"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    payment_id = db.Column(
        db.Integer,
        db.ForeignKey("donor_payments.id"),
        nullable=False
    )

    document_name = db.Column(
        db.String(255),
        nullable=False
    )

    document_type = db.Column(
        db.String(50),
        nullable=False
    )

    file_url = db.Column(
        db.Text
    )

    file_path = db.Column(
        db.Text
    )

    file_size = db.Column(
        db.String(30)
    )

    verification_status = db.Column(
        db.String(30),
        default="Pending"
    )

    uploaded_by = db.Column(
        db.String(150)
    )

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "payment_id": self.payment_id,
            "name": self.document_name,
            "type": self.document_type,
            "url": self.file_url,
            "size": self.file_size,
            "status": self.verification_status,
            "uploaded_by": self.uploaded_by,
            "uploaded_at": (
                self.uploaded_at.isoformat()
                if self.uploaded_at
                else None
            ),
        }