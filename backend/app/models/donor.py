from app.extensions import db
from app.models.base import BaseModel


class Donor(BaseModel):
    __tablename__ = "donors"

    name = db.Column(db.String(200), nullable=False)
    focus_area = db.Column(db.String(150))
    likelihood = db.Column(db.Integer, default=0)
    last_contact = db.Column(db.Date)
    logo_url = db.Column(db.String(300))

    # health of the relationship: healthy | warning | critical
    status = db.Column(db.String(30), default="healthy")

    def __repr__(self):
        return f"<Donor {self.name}>"
