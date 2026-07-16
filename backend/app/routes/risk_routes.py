from datetime import date

from flask import Blueprint, jsonify

from app.models.risk import Risk

risk_bp = Blueprint("risks", __name__)


def _time_left(due):
    if not due:
        return None

    days = max((due - date.today()).days, 0)

    if days == 1:
        return "1 day"

    return f"{days} days"


@risk_bp.route("/risks", methods=["GET"])
def get_risks():
    # Preserve insertion order so the feed reads like the design.
    risks = Risk.query.order_by(Risk.id.asc()).all()

    return jsonify(
        [
            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "level": r.level,
                "time_left": _time_left(r.due_date),
                "action": r.action,
                "icon": r.icon,
            }
            for r in risks
        ]
    )
