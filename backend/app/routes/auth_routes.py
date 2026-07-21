from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()

    if not user or not user.is_active or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    return jsonify(
        {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.name if user.role else None,
        }
    )
