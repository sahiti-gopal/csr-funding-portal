from app.extensions import db
from app.models.base import BaseModel


class BeneficiaryCategory(BaseModel):
    __tablename__ = "beneficiary_categories"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(100))
    color = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<BeneficiaryCategory {self.name}>"