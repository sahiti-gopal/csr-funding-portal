from flask import Blueprint, jsonify

from app.models.donor import Donor
from app.models.donor_payment import DonorPayment
from app.models.project import Project
from app.models.project_type import ProjectType
from app.routes.dashboard_routes import PROJECT_TYPE_SDG_MAP
from app.services.ai_summary import generate_ai_json

donor_bp = Blueprint("donors", __name__)

NEEDS_ATTENTION_STATUSES = ["Planning", "Pending", "On Hold"]

DONOR_AI_SYSTEM_PROMPT = (
    "You are a CSR relationship analyst. Given JSON data about one corporate "
    "donor's projects and payments, write a JSON object with exactly these "
    "keys: "
    '"engagement_summary" (2-3 sentence plain-English summary of how engaged '
    "this donor currently is, referencing their status/likelihood/last "
    "contact), "
    '"key_risks" (a list of 1-4 short strings, each one concrete risk drawn '
    "only from the numbers given — overdue payments, low fund utilization, "
    "projects needing attention. If nothing is concerning, return a single "
    'item saying no significant risks were found), '
    '"project_health_summary" (2-3 sentences on the health of this donor\'s '
    "funded projects — utilization, beneficiaries reached, project status "
    "mix). "
    "Use ONLY the numbers given — never invent or estimate a number that "
    "isn't present. Do not mention SQL, databases, or JSON in the text "
    "itself."
)

def _donor_stats(donor_id):
    projects = Project.query.filter(Project.donor_id == donor_id).all()
    payments = DonorPayment.query.filter_by(donor_id=donor_id).all()

    budget_total = sum(float(p.budget or 0) for p in projects)
    raised_total = sum(float(p.raised_amount or 0) for p in projects)
    utilized_total = sum(float(p.utilized_amount or 0) for p in projects)
    beneficiaries_total = sum(p.beneficiaries_reached or 0 for p in projects)

    overdue_payments = [p for p in payments if p.status == "Overdue"]
    pending_payments = [p for p in payments if p.status in ("Pending", "Scheduled")]
    paid_payments = [p for p in payments if p.status == "Paid"]

    next_due = min(
        (p.due_date for p in payments if p.due_date and p.status != "Paid"),
        default=None,
    )

    return {
        "projects_total": len(projects),
        "projects_active": sum(1 for p in projects if p.status == "Active"),
        "projects_completed": sum(1 for p in projects if p.status == "Completed"),
        "projects_needs_attention": sum(
            1 for p in projects if p.status in NEEDS_ATTENTION_STATUSES
        ),
        "budget_total": budget_total,
        "raised_total": raised_total,
        "utilized_total": utilized_total,
        "utilization_pct": (
            round(utilized_total / raised_total * 100) if raised_total else 0
        ),
        "beneficiaries_total": beneficiaries_total,
        "payments_total": len(payments),
        "payments_overdue": len(overdue_payments),
        "payments_pending": len(pending_payments),
        "payments_paid": len(paid_payments),
        "next_payment_due": next_due.isoformat() if next_due else None,
        "projects": [
            {
                "id": p.id,
                "name": p.project_name,
                "status": p.status,
                "budget": float(p.budget or 0),
                "raised_amount": float(p.raised_amount or 0),
                "utilized_amount": float(p.utilized_amount or 0),
                "beneficiaries_reached": p.beneficiaries_reached or 0,
                "region": p.region,
                "financial_year": p.financial_year,
            }
            for p in projects
        ],
    }


def _fallback_donor_summary(donor, stats):
    risks = []

    if stats["payments_overdue"]:
        risks.append(
            f"{stats['payments_overdue']} overdue payment"
            f"{'s' if stats['payments_overdue'] != 1 else ''} pending follow-up."
        )

    if stats["raised_total"] and stats["utilization_pct"] < 50:
        risks.append(
            f"Fund utilization is at only {stats['utilization_pct']}% of funds raised."
        )

    if stats["projects_needs_attention"]:
        risks.append(
            f"{stats['projects_needs_attention']} project"
            f"{'s' if stats['projects_needs_attention'] != 1 else ''} flagged as "
            "needing attention."
        )

    if not risks:
        risks.append("No significant risks flagged from available payment and project data.")

    last_contact = donor.last_contact.isoformat() if donor.last_contact else "never"

    return {
        "engagement_summary": (
            f"{donor.name} is currently marked {donor.status or 'unknown'} with a "
            f"{donor.likelihood or 0}% likelihood score; last contacted {last_contact}."
        ),
        "key_risks": risks,
        "project_health_summary": (
            f"Across {stats['projects_total']} project(s), "
            f"{stats['utilization_pct']}% of raised funds have been utilized, "
            f"reaching {stats['beneficiaries_total']} beneficiaries."
        ),
    }


@donor_bp.route("/donors", methods=["GET"])
def get_donors():
    donors = Donor.query.order_by(Donor.likelihood.desc()).all()

    return jsonify(
        [
            {
                "id": d.id,
                "name": d.name,
                "focus_area": d.focus_area,
                "logo_url": d.logo_url,
                "likelihood": d.likelihood,
                "last_contact": (
                    str(d.last_contact) if d.last_contact else None
                ),
                "status": d.status,
            }
            for d in donors
        ]
    )


@donor_bp.route("/donors/<int:donor_id>", methods=["GET"])
def get_donor(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    stats = _donor_stats(donor_id)

    return jsonify(
        {
            "id": donor.id,
            "name": donor.name,
            "focus_area": donor.focus_area,
            "logo_url": donor.logo_url,
            "likelihood": donor.likelihood,
            "last_contact": (
                str(donor.last_contact) if donor.last_contact else None
            ),
            "status": donor.status,
            **stats,
        }
    )


@donor_bp.route("/donors/<int:donor_id>/ai-summary", methods=["GET"])
def donor_ai_summary(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    stats = _donor_stats(donor_id)

    ai = generate_ai_json(
        DONOR_AI_SYSTEM_PROMPT,
        {
            "donor_name": donor.name,
            "donor_status": donor.status,
            "donor_likelihood": donor.likelihood,
            "donor_last_contact": (
                str(donor.last_contact) if donor.last_contact else None
            ),
            **{k: v for k, v in stats.items() if k != "projects"},
        },
    )

    required_keys = ("engagement_summary", "key_risks", "project_health_summary")

    if ai and all(k in ai for k in required_keys):
        return jsonify({**ai, "ai_generated": True, "stats": stats})

    fallback = _fallback_donor_summary(donor, stats)
    return jsonify({**fallback, "ai_generated": False, "stats": stats})


@donor_bp.route("/donors/<int:donor_id>/sdg-impact", methods=["GET"])
def donor_sdg_impact(donor_id):
    # Same project-type -> SDG mapping used for the overall Overview band,
    # just scoped to this donor's own funded projects — so the highlighted
    # goals are always a subset of the goals funded org-wide.
    funded_type_names = (
        Project.query
        .filter(Project.donor_id == donor_id, Project.raised_amount > 0)
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

    return jsonify({"funded_sdg_ids": funded_sdg_ids})
