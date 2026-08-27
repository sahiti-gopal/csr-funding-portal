from flask import Blueprint, jsonify, request
from sqlalchemy import func

from app.extensions import db
from app.models.project import Project
from app.models.project_type import ProjectType
from app.models.donor import Donor
from app.services.ai_summary import generate_ai_json
from app.utils.format import format_inr, format_count

dashboard_bp = Blueprint("dashboard", __name__)

DASHBOARD_AI_SYSTEM_PROMPT = (
    "You are a CSR portfolio analyst. Given JSON aggregate data about a "
    "company's overall CSR donor and project portfolio, write a JSON object "
    'with exactly one key, "summary", holding a 3-4 sentence plain-English '
    "executive summary of overall donor engagement health and where "
    "attention is needed most. Use ONLY the numbers given — never invent or "
    "estimate a number that isn't present. Every field ending in "
    '"_formatted" is the Indian-style abbreviated form (Cr for crore, L for '
    "lakh) of the field with the same base name — when the summary mentions "
    "that figure, use the _formatted value verbatim (e.g. \"₹1.8 Cr\") "
    "instead of writing out the full number, so the text never shows a long "
    "run of digits. Do not mention SQL, databases, or JSON in the text "
    "itself."
)

# Rough mapping from this app's project types to the UN SDG goals they
# most directly serve. Used only to mark a goal "funded" on the Overview
# SDG band — not an official/exhaustive SDG classification.
PROJECT_TYPE_SDG_MAP = {
    "Education": [4, 10],
    "Healthcare": [3, 6],
    "Environment": [13, 15],
    "Women Empowerment": [5],
    "Livelihood": [1, 8],
    "Skill Development": [4, 8],
    "Rural Development": [11],
}


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

    funded_type_names = (
        query.filter(Project.raised_amount > 0)
        .join(ProjectType)
        .with_entities(ProjectType.name)
        .distinct()
        .all()
    )

    funded_sdg_ids = sorted({
        sdg_id
        for (type_name,) in funded_type_names
        for sdg_id in PROJECT_TYPE_SDG_MAP.get(type_name, [])
    })

    type_donor_stats = (
        query.filter(Project.raised_amount > 0)
        .join(ProjectType)
        .join(Donor)
        .with_entities(
            ProjectType.name,
            Donor.id,
            Donor.name,
            Donor.logo_url,
            func.sum(Project.raised_amount),
            func.count(Project.id),
            func.coalesce(func.sum(Project.beneficiaries_reached), 0),
        )
        .group_by(ProjectType.name, Donor.id, Donor.name, Donor.logo_url)
        .all()
    )

    sdg_stats = {}

    for type_name, donor_id, donor_name, logo_url, amount, project_count, goal_beneficiaries in type_donor_stats:
        for sdg_id in PROJECT_TYPE_SDG_MAP.get(type_name, []):
            bucket = sdg_stats.setdefault(
                sdg_id, {"projects": 0, "beneficiaries": 0, "partners": {}}
            )
            bucket["projects"] += project_count
            bucket["beneficiaries"] += goal_beneficiaries
            partner = bucket["partners"].setdefault(
                donor_id, {"name": donor_name, "logo_url": logo_url, "amount": 0}
            )
            partner["amount"] += amount

    sdg_impact_details = {
        str(sdg_id): {
            "projects": data["projects"],
            "beneficiaries": int(data["beneficiaries"]),
            "partners": [
                {
                    "name": partner["name"],
                    "logo_url": partner["logo_url"],
                    "amount": float(partner["amount"]),
                }
                for partner in sorted(
                    data["partners"].values(),
                    key=lambda p: p["amount"],
                    reverse=True,
                )
            ],
        }
        for sdg_id, data in sdg_stats.items()
    }

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
            "funded_sdg_ids": funded_sdg_ids,
            "sdg_impact_details": sdg_impact_details,
        }
    )
from app.models.donor import Donor


def _fallback_dashboard_summary(stats):
    return (
        f"{stats['sponsors']} sponsors are funding {stats['funded']} active "
        f"project(s) ({stats['completed']} completed, "
        f"{stats['needs_attention']} needing attention), with "
        f"{stats['utilization_pct']}% of {format_inr(stats['raised_amount'])} raised "
        f"utilized so far, reaching {format_count(stats['beneficiaries'])} beneficiaries. "
        f"Average donor likelihood score is {stats['avg_donor_likelihood']}%."
    )


@dashboard_bp.route("/dashboard/ai-summary", methods=["GET"])
def ai_summary():
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

    funded = query.filter(Project.status == "Active").count()
    completed = query.filter(Project.status == "Completed").count()
    needs_attention = query.filter(
        Project.status.in_(["Planning", "Pending", "On Hold"])
    ).count()

    sponsors = Donor.query.count()
    avg_likelihood = db.session.query(
        func.coalesce(func.avg(Donor.likelihood), 0)
    ).scalar()

    donor_status_counts = dict(
        db.session.query(Donor.status, func.count(Donor.id))
        .group_by(Donor.status)
        .all()
    )

    stats = {
        "region": region,
        "financial_year": fy,
        "raised_amount": float(raised),
        "utilized_amount": float(utilized),
        "utilization_pct": (
            round((utilized / raised) * 100) if raised else 0
        ),
        "beneficiaries": int(beneficiaries),
        "funded": funded,
        "completed": completed,
        "needs_attention": needs_attention,
        "sponsors": sponsors,
        "avg_donor_likelihood": round(float(avg_likelihood)),
        "donor_status_counts": donor_status_counts,
    }

    # Abbreviated companion fields for the AI prompt only (see
    # DASHBOARD_AI_SYSTEM_PROMPT) — kept out of the stats returned to the
    # frontend/stored on the summary payload since the UI formats these
    # itself (frontend/src/utils/format.js) from the raw figures.
    ai_stats = {
        **stats,
        "raised_amount_formatted": format_inr(stats["raised_amount"]),
        "utilized_amount_formatted": format_inr(stats["utilized_amount"]),
        "beneficiaries_formatted": format_count(stats["beneficiaries"]),
    }

    ai = generate_ai_json(DASHBOARD_AI_SYSTEM_PROMPT, ai_stats)

    if ai and "summary" in ai:
        return jsonify({"summary": ai["summary"], "ai_generated": True, "stats": stats})

    return jsonify(
        {
            "summary": _fallback_dashboard_summary(stats),
            "ai_generated": False,
            "stats": stats,
        }
    )


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