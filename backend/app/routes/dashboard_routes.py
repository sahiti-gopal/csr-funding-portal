from flask import Blueprint, jsonify, request
from sqlalchemy import func

from app.extensions import db
from app.models.project import Project
from app.models.donor import Donor

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard/summary", methods=["GET"])
def summary():

    region = request.args.get("region", "all")
    fy = request.args.get("fy", "all")

    query = Project.query

    if region != "all":
        query = query.filter(Project.region == region)

    if fy != "all":
        query = query.filter(Project.financial_year == fy)

    raised = query.with_entities(
        func.coalesce(func.sum(Project.raised_amount), 0)
    ).scalar()

    utilized = query.with_entities(
        func.coalesce(func.sum(Project.utilized_amount), 0)
    ).scalar()

    beneficiaries = query.with_entities(
        func.coalesce(func.sum(Project.beneficiaries_reached), 0)
    ).scalar()

    funded = query.filter(
    Project.status == "Active"
    ).count()

    registered = query.filter(
        Project.status == "Registered"
    ).count()

    completed = query.filter(
        Project.status == "Completed"
    ).count()

    needs_attention = query.filter(
        Project.status.in_(["Planning", "Pending", "On Hold"])
    ).count()

    sponsors = Donor.query.count()

    utilization_pct = (
        round((utilized / raised) * 100)
        if raised
        else 0
    )

    return jsonify(
        {
            "raised_amount": float(raised),
            "utilized_amount": float(utilized),
            "utilization_pct": utilization_pct,
            "beneficiaries": int(beneficiaries),
            "registered": registered,
            "funded": funded,
            "completed": completed,
            "needs_attention": needs_attention,
            "sponsors": sponsors,
        }
    )
from app.models.donor import Donor


@dashboard_bp.route("/dashboard/donor-readiness", methods=["GET"])
def donor_readiness():

    donors = (
        Donor.query
        .order_by(
            Donor.likelihood.desc(),
            Donor.last_contact.asc()
        )
        .limit(5)
        .all()
    )

    return jsonify([
        {
            "id": donor.id,
            "name": donor.name,
            "focus_area": donor.focus_area,
            "likelihood": donor.likelihood,
            "last_contact": donor.last_contact.strftime("%d %b %Y")
            if donor.last_contact
            else "Never",

            "status": donor.status
        }

        for donor in donors
    ])