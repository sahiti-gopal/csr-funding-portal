from app.extensions import db
from app.models.base import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    users = db.relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"