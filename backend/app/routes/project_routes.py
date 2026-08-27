import os

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from datetime import datetime

from app.extensions import db
from app.models.project import Project
from sqlalchemy import or_
from app.models.project_type import ProjectType
from app.models.beneficiary_category import BeneficiaryCategory
from app.models.donor import Donor

project_bp = Blueprint("projects", __name__)

# Project documents (seeded ProjectDocument rows and the fallback pool below
# alike) only ever use this small, fixed set of display names — mapped to a
# real sample file under app/static/sample_documents/ (see
# generate_sample_documents.py) so "Recent Files" has something genuine to
# preview instead of just a name+size record with no file behind it.
DOCUMENT_SAMPLE_FILES = {
    "Project Proposal.pdf": "project_proposal.pdf",
    "Progress Report.pdf": "progress_report.pdf",
    "MOU Agreement.pdf": "mou_agreement.pdf",
    "Q2 Impact Report.pdf": "q2_impact_report.pdf",
    "Budget Estimate.xlsx": "budget_estimate.xlsx",
    "Budget Breakdown.xlsx": "budget_breakdown.xlsx",
}


def _document_url(name):
    filename = DOCUMENT_SAMPLE_FILES.get(name)
    return f"/api/projects/documents/file/{filename}" if filename else None

# Per-project-type breakdown of a project's `beneficiaries_reached` total
# into 3 KPI tiles, used when no ProjectMetric rows were seeded for a project.
FALLBACK_METRIC_TEMPLATES = {
    "Education": [
        ("students", "Students Reached", 1),
        ("schools", "Schools Covered", 150),
        ("teachers", "Teachers Trained", 30),
    ],
    "Healthcare": [
        ("patients", "Patients Treated", 1),
        ("camps", "Health Camps Conducted", 100),
        ("volunteers", "Volunteers Deployed", 50),
    ],
    "Environment": [
        ("beneficiaries", "People Impacted", 1),
        ("sites", "Sites Covered", 80),
        ("volunteers", "Volunteers Deployed", 40),
    ],
    "Women Empowerment": [
        ("beneficiaries", "Women Reached", 1),
        ("trainings", "Training Sessions", 60),
        ("teachers", "Trainers Deployed", 40),
    ],
    "Livelihood": [
        ("beneficiaries", "Individuals Supported", 1),
        ("sites", "Communities Covered", 70),
        ("volunteers", "Field Officers", 35),
    ],
    "Skill Development": [
        ("beneficiaries", "Youth Trained", 1),
        ("trainings", "Training Batches", 50),
        ("teachers", "Trainers Deployed", 25),
    ],
    "Rural Development": [
        ("beneficiaries", "Households Reached", 1),
        ("sites", "Villages Covered", 60),
        ("volunteers", "Field Volunteers", 30),
    ],
}

DEFAULT_METRIC_TEMPLATE = [
    ("beneficiaries", "Beneficiaries Reached", 1),
    ("sites", "Locations Covered", 75),
    ("volunteers", "Volunteers Deployed", 40),
]


def fallback_beneficiary_metrics(p):
    reached = p.beneficiaries_reached or 0
    template = FALLBACK_METRIC_TEMPLATES.get(
        p.project_type.name, DEFAULT_METRIC_TEMPLATE
    )

    metrics = []
    for icon, title, divisor in template:
        value = max(1, reached // divisor) if reached else 0
        target = max(value + 1, round(value * 1.25))
        metrics.append(
            {"icon": icon, "title": title, "value": value, "target": target}
        )
    return metrics


# Names line up with actual files in frontend/public/images/team/
TEAM_NAME_POOL = [
    "Priya Sharma",
    "Rohan Mehta",
    "Pooja Nair",
    "Vivek Menon",
    "Kavita Rao",
]

SECONDARY_ROLE_POOL = [
    ("Field Coordinator", "Ops"),
    ("Program Manager", "Lead"),
    ("Training Lead", "Training"),
]

DOCUMENT_POOL = [
    ("Project Proposal.pdf", "1.2 MB"),
    ("Budget Estimate.xlsx", "640 KB"),
    ("Progress Report.pdf", "2.1 MB"),
    ("MOU Agreement.pdf", "890 KB"),
]


def fallback_team(p):
    owner_name = TEAM_NAME_POOL[p.id % len(TEAM_NAME_POOL)]
    second_name = TEAM_NAME_POOL[(p.id + 1) % len(TEAM_NAME_POOL)]
    second_role, second_tag = SECONDARY_ROLE_POOL[p.id % len(SECONDARY_ROLE_POOL)]

    return [
        {"name": owner_name, "role": "Project Manager", "tag": "Lead"},
        {"name": second_name, "role": second_role, "tag": second_tag},
    ]


def fallback_documents(p):
    return [
        {"name": name, "size": size, "url": _document_url(name)}
        for name, size in (
            DOCUMENT_POOL[p.id % len(DOCUMENT_POOL):]
            + DOCUMENT_POOL[: p.id % len(DOCUMENT_POOL)]
        )[:3]
    ]


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
        .outerjoin(Donor, Project.donor_id == Donor.id)
    )

    if search:
        query = query.filter(
            or_(
                Project.project_name.ilike(f"%{search}%"),
                Project.location.ilike(f"%{search}%"),
                Donor.name.ilike(f"%{search}%"),
                Donor.focus_area.ilike(f"%{search}%"),
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
                "sponsor_name": p.donor.name if p.donor else None,
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
    if p.donor:
        parts = ["CSR Partner"]
        if p.donor.focus_area:
            parts.append(p.donor.focus_area)
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
                {
                    "name": p.donor.name,
                    "meta": sponsor_meta,
                    "grant_amount": p.budget,
                    "contract_period": (
                        f"{p.start_date.year}-{p.end_date.year}"
                        if p.start_date and p.end_date
                        else None
                    ),
                }
                if p.donor
                else None
            ),
            "beneficiaries": (
                [
                    {
                        "icon": m.icon,
                        "title": m.title,
                        "value": m.current_value,
                        "target": m.target_value,
                    }
                    for m in p.metrics
                ]
                if p.metrics
                else fallback_beneficiary_metrics(p)
            ),
            "locations": (
                [loc.name for loc in p.locations]
                if p.locations
                else ([p.location] if p.location else [])
            ),
            "team": (
                [
                    {"name": t.name, "role": t.role, "tag": t.tag}
                    for t in p.team_members
                ]
                if p.team_members
                else fallback_team(p)
            ),
            "documents": (
                [
                    {"name": d.name, "size": d.size, "url": _document_url(d.name)}
                    for d in p.documents
                ]
                if p.documents
                else fallback_documents(p)
            ),
        }
    )


@project_bp.route("/projects/documents/file/<path:filename>", methods=["GET"])
def get_project_document_file(filename):
    # Only ever serves the fixed sample files above (never an arbitrary path
    # off disk) — filename always comes from DOCUMENT_SAMPLE_FILES' own
    # values, not directly from user input.
    if filename not in DOCUMENT_SAMPLE_FILES.values():
        return jsonify({"message": "File not found"}), 404

    sample_dir = os.path.join(current_app.static_folder, "sample_documents")
    return send_from_directory(sample_dir, filename)


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
