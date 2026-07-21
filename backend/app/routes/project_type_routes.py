from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.project_type import ProjectType

project_type_bp = Blueprint("project_types", __name__)


def _serialize(p):
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "icon": p.icon,
        "color": p.color,
        "is_active": p.is_active,
        "project_count": len(p.projects),
    }


@project_type_bp.get("/project-types")
def get_project_types():
    project_types = ProjectType.query.all()
    return jsonify([_serialize(p) for p in project_types])


@project_type_bp.route("/project-types", methods=["POST"])
def create_project_type():
    data = request.get_json()

    project_type = ProjectType(
        name=data["name"],
        description=data.get("description"),
        icon=data.get("icon"),
        color=data.get("color"),
    )

    db.session.add(project_type)
    db.session.commit()

    return jsonify(_serialize(project_type)), 201


@project_type_bp.route("/project-types/<int:id>", methods=["PUT"])
def update_project_type(id):
    data = request.get_json()
    project_type = ProjectType.query.get_or_404(id)

    project_type.name = data["name"]
    project_type.description = data.get("description")

    db.session.commit()

    return jsonify(_serialize(project_type))


@project_type_bp.route("/project-types/<int:id>", methods=["DELETE"])
def delete_project_type(id):
    project_type = ProjectType.query.get_or_404(id)

    if project_type.projects:
        return jsonify(
            {"message": "Cannot delete a project type that has projects assigned to it."}
        ), 409

    db.session.delete(project_type)
    db.session.commit()

    return jsonify({"message": "Project type deleted successfully"})
