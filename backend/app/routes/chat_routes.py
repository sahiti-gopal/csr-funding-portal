from flask import Blueprint, jsonify, request
from sqlalchemy import func

from app.config import Config
from app.models.project import Project
from app.models.donor import Donor
from app.models.alert import Alert
from app.models.risk import Risk

chat_bp = Blueprint("chat", __name__)

PAGE_LABELS = {
    "/": "Dashboard",
    "/projects": "Projects",
    "/alerts": "Alerts",
    "/donors": "Donors",
    "/reports": "Reports",
    "/analytics": "Analytics",
    "/settings": "Settings",
}


def _build_context():
    raised = Project.query.with_entities(
        func.coalesce(func.sum(Project.raised_amount), 0)
    ).scalar()
    utilized = Project.query.with_entities(
        func.coalesce(func.sum(Project.utilized_amount), 0)
    ).scalar()
    beneficiaries = Project.query.with_entities(
        func.coalesce(func.sum(Project.beneficiaries_reached), 0)
    ).scalar()

    project_counts = {
        status: Project.query.filter(Project.status == status).count()
        for status in ["Active", "Registered", "Completed", "Planning", "Pending", "On Hold"]
    }

    recent_projects = (
        Project.query.order_by(Project.updated_at.desc()).limit(5).all()
    )

    alerts_total = Alert.query.count()
    alerts_unread = Alert.query.filter_by(is_read=False).count()
    alerts_high = Alert.query.filter_by(priority="HIGH").count()

    risks = Risk.query.order_by(Risk.id.asc()).limit(5).all()

    donors_total = Donor.query.count()
    top_donors = (
        Donor.query.order_by(Donor.likelihood.desc()).limit(5).all()
    )

    return {
        "totals": {
            "raised_amount": float(raised),
            "utilized_amount": float(utilized),
            "beneficiaries_reached": int(beneficiaries),
            "donors": donors_total,
        },
        "project_status_counts": project_counts,
        "recent_projects": [
            {
                "name": p.name,
                "status": p.status,
                "raised_amount": float(p.raised_amount or 0),
                "utilized_amount": float(p.utilized_amount or 0),
            }
            for p in recent_projects
        ],
        "alerts": {
            "total": alerts_total,
            "unread": alerts_unread,
            "high_priority": alerts_high,
        },
        "top_risks": [
            {"title": r.title, "level": r.level, "action": r.action}
            for r in risks
        ],
        "top_donors": [
            {"name": d.name, "focus_area": d.focus_area, "status": d.status}
            for d in top_donors
        ],
    }


@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    page_path = data.get("page") or "/"

    if not message:
        return jsonify({"error": "message is required"}), 400

    if not Config.ANTHROPIC_API_KEY:
        return jsonify(
            {"error": "AI assistant is not configured. Set ANTHROPIC_API_KEY in backend/.env."}
        ), 503

    try:
        import anthropic
    except ImportError:
        return jsonify(
            {"error": "The 'anthropic' package is not installed. Run pip install -r requirements.txt."}
        ), 503

    context = _build_context()
    page_label = PAGE_LABELS.get(page_path, page_path)

    system_prompt = (
        "You are the in-app assistant for the CSR Funding Portal, a corporate "
        "social responsibility project-tracking dashboard. Answer the user's "
        "question using the live data snapshot below. Be concise and concrete. "
        "If the data doesn't cover the question, say so instead of guessing.\n\n"
        f"The user is currently viewing the '{page_label}' page.\n\n"
        f"Data snapshot (JSON): {context}"
    )

    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            system=system_prompt,
            messages=[{"role": "user", "content": message}],
        )
        reply = "".join(
            block.text for block in response.content if block.type == "text"
        )
    except Exception as exc:
        return jsonify({"error": f"AI request failed: {exc}"}), 502

    return jsonify({"reply": reply, "page": page_label})
