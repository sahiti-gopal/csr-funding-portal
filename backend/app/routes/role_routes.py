from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.role import Role

role_bp = Blueprint("roles", __name__)


def _serialize(r):
    return {
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "is_active": r.is_active,
        "user_count": len(r.users),
    }


@role_bp.get("/roles")
def get_roles():
    roles = Role.query.all()
    return jsonify([_serialize(r) for r in roles])


@role_bp.route("/roles", methods=["POST"])
def create_role():
    data = request.get_json()

    role = Role(
        name=data["name"],
        description=data.get("description"),
    )

    db.session.add(role)
    db.session.commit()

    return jsonify(_serialize(role)), 201


@role_bp.route("/roles/<int:id>", methods=["PUT"])
def update_role(id):
    data = request.get_json()
    role = Role.query.get_or_404(id)

    role.name = data["name"]
    role.description = data.get("description")

    db.session.commit()

    return jsonify(_serialize(role))


@role_bp.route("/roles/<int:id>", methods=["DELETE"])
def delete_role(id):
    role = Role.query.get_or_404(id)

    if role.users:
        return jsonify(
            {"message": "Cannot delete a role that has users assigned to it."}
        ), 409

    db.session.delete(role)
    db.session.commit()

    return jsonify({"message": "Role deleted successfully"})
