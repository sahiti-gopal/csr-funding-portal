from app.extensions import db
from app.models.base import BaseModel


class DonorDocument(BaseModel):
    __tablename__ = "donor_documents"

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("donors.id"),
        nullable=False,
    )

    category = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date)
    severity = db.Column(db.String(20), default="Medium")

    # Missing | Requested | Pending Review | Verified
    status = db.Column(db.String(30), default="Missing")

    owner = db.Column(db.String(150))
    file_path = db.Column(db.Text)
    file_size = db.Column(db.String(30))
    uploaded_at = db.Column(db.DateTime)

    donor = db.relationship(
        "Donor",
        backref=db.backref(
            "documents",
            cascade="all, delete-orphan",
            order_by="DonorDocument.id",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "donorId": self.donor_id,
            "category": self.category,
            "title": self.title,
            "due": self.due_date.isoformat() if self.due_date else None,
            "severity": self.severity,
            "status": self.status,
            "owner": self.owner,
            "fileUrl": f"/api/documents/{self.id}/file" if self.file_path else None,
            "fileSize": self.file_size,
            "uploadedAt": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }

    def __repr__(self):
        return f"<DonorDocument {self.title}>"
