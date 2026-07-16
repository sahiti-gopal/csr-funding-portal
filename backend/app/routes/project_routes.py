from flask import Blueprint, jsonify, request
from datetime import datetime

from app.extensions import db
from app.models.project import Project
from sqlalchemy import or_
from app.models.project_type import ProjectType
from app.models.beneficiary_category import BeneficiaryCategory

project_bp = Blueprint("projects", __name__)


# ==========================
# GET ALL PROJECTS
# ==========================
@project_bp.route("/projects", methods=["GET"])
def get_projects():

    search = request.args.get("search", "").strip()
    region = request.args.get("region", "all")
    fy = request.args.get("fy", "all")
    status = request.args.get("status", "all")

    query = (
        Project.query
        .join(ProjectType)
        .join(BeneficiaryCategory)
    )

    if search:
        query = query.filter(
            or_(
                Project.project_name.ilike(f"%{search}%"),
                Project.location.ilike(f"%{search}%"),
                Project.sponsor_name.ilike(f"%{search}%"),
                Project.sponsor_sector.ilike(f"%{search}%"),
                ProjectType.name.ilike(f"%{search}%"),
                BeneficiaryCategory.name.ilike(f"%{search}%")
            )
        )

    if region != "all":
        query = query.filter(Project.region == region)

    if fy != "all":
        query = query.filter(Project.financial_year == fy)

    if status != "all":
        query = query.filter(Project.status == status)

    projects = query.order_by(Project.project_name).all()

    data = []

    for p in projects:
        data.append(
            {
                "id": p.id,
                "project_name": p.project_name,
                "project_type": p.project_type.name,
                "beneficiary_category": p.beneficiary_category.name,
                "project_type_id": p.project_type_id,
                "beneficiary_category_id": p.beneficiary_category_id,
                "budget": p.budget,
                "location": p.location,
                "status": p.status,
                "region": p.region,
                "financial_year": p.financial_year,
                "sponsor_name": p.sponsor_name,
                "raised_amount": p.raised_amount,
                "utilized_amount": p.utilized_amount,
                "beneficiaries_reached": p.beneficiaries_reached,
                "start_date": str(p.start_date),
                "end_date": str(p.end_date),
            }
        )

    return jsonify(data)

# ==========================
# GET SINGLE PROJECT (detail)
# ==========================
@project_bp.route("/projects/<int:id>", methods=["GET"])
def get_project(id):
    p = Project.query.get_or_404(id)

    sponsor_meta = None
    if p.sponsor_name:
        parts = ["CSR Partner"]
        if p.sponsor_sector:
            parts.append(p.sponsor_sector)
        sponsor_meta = " · ".join(parts)

    return jsonify(
        {
            "id": p.id,
            "project_name": p.project_name,
            "project_type": p.project_type.name,
            "beneficiary_category": p.beneficiary_category.name,
            "project_type_id": p.project_type_id,
            "beneficiary_category_id": p.beneficiary_category_id,
            "budget": p.budget,
            "location": p.location,
            "status": p.status,
            "start_date": str(p.start_date),
            "end_date": str(p.end_date),
            "sponsor": (
                {"name": p.sponsor_name, "meta": sponsor_meta}
                if p.sponsor_name
                else None
            ),
            "beneficiaries": [
                {
                    "icon": m.icon,
                    "title": m.title,
                    "value": m.current_value,
                    "target": m.target_value,
                }
                for m in p.metrics
            ],
            "locations": [loc.name for loc in p.locations],
            "team": [
                {"name": t.name, "role": t.role, "tag": t.tag} for t in p.team_members
            ],
            "documents": [{"name": d.name, "size": d.size} for d in p.documents],
        }
    )


# ==========================
# CREATE PROJECT
# ==========================
@project_bp.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()

    project = Project(
        project_name=data["project_name"],
        project_type_id=int(data["project_type_id"]),
        beneficiary_category_id=int(data["beneficiary_category_id"]),
        budget=float(data["budget"]),
        location=data["location"],
        status=data["status"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
    )

    db.session.add(project)
    db.session.commit()

    return (
        jsonify(
            {
                "id": project.id,
                "message": "Project created successfully",
            }
        ),
        201,
    )


# ==========================
# UPDATE PROJECT
# ==========================
@project_bp.route("/projects/<int:id>", methods=["PUT"])
def update_project(id):
    data = request.get_json()

    project = Project.query.get_or_404(id)

    project.project_name = data["project_name"]
    project.project_type_id = int(data["project_type_id"])
    project.beneficiary_category_id = int(data["beneficiary_category_id"])
    project.budget = float(data["budget"])
    project.location = data["location"]
    project.status = data["status"]
    project.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    project.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()

    db.session.commit()

    return jsonify(
        {
            "message": "Project updated successfully",
        }
    )


# ==========================
# DELETE PROJECT
# ==========================
@project_bp.route("/projects/<int:id>", methods=["DELETE"])
def delete_project(id):
    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    return jsonify(
        {
            "message": "Project deleted successfully",
        }
    )
