from flask import Blueprint, jsonify
from app.models.project_type import ProjectType

project_type_bp = Blueprint("project_types", __name__)

@project_type_bp.get("/project-types")
def get_project_types():

    project_types = ProjectType.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "icon": p.icon,
            "color": p.color,
            "is_active": p.is_active
        }
        for p in project_types
    ])