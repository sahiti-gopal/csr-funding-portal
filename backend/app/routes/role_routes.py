from flask import Blueprint, jsonify
from app.models.role import Role

role_bp = Blueprint("roles", __name__)


@role_bp.get("/roles")
def get_roles():

    roles = Role.query.all()

    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "is_active": r.is_active
        }
        for r in roles
    ])