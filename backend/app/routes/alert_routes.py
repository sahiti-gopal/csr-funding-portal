from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from app.extensions import db
from app.models.alert import Alert

alert_bp = Blueprint("alerts", __name__)

# ==========================
# GET ALL ALERTS
# ==========================

@alert_bp.route("/alerts", methods=["GET"])
def get_alerts():

    search = request.args.get("search", "")
    priority = request.args.get("priority", "All")

    query = Alert.query

    if search:
        query = query.filter(
            or_(
                Alert.title.ilike(f"%{search}%"),
                Alert.description.ilike(f"%{search}%")
            )
        )

    if priority != "All":
        query = query.filter(
            Alert.priority == priority.upper()
        )

    alerts = (
        query.order_by(Alert.created_at.desc())
        .all()
    )

    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "category": a.category,
            "priority": a.priority,
            "status": a.status,
            "is_read": a.is_read,
            "is_resolved": a.is_resolved,
            "due_date": a.due_date.strftime("%d %b %Y")
            if a.due_date else None,
            "project_name": a.project.project_name
            if a.project else None,
        }
        for a in alerts
    ])
# ==========================
# SUMMARY
# ==========================

@alert_bp.route("/alerts/summary", methods=["GET"])
def summary():

    total = Alert.query.count()

    high = Alert.query.filter_by(
        priority="HIGH"
    ).count()

    medium = Alert.query.filter_by(
        priority="MEDIUM"
    ).count()

    low = Alert.query.filter_by(
        priority="LOW"
    ).count()

    return jsonify({

        "total": total,

        "high": high,

        "medium": medium,

        "low": low

    })
# ==========================
# MARK READ
# ==========================
@alert_bp.route("/alerts/mark-all-read", methods=["POST"])
def mark_all_read():

    Alert.query.update(
        {
            Alert.is_read: True
        }
    )

    db.session.commit()

    return jsonify(
        {
            "success": True
        }
    )

@alert_bp.patch("/alerts/<int:id>/read")
def mark_read(id):

    alert = Alert.query.get_or_404(id)

    alert.is_read = True

    alert.status = "Read"

    db.session.commit()

    return jsonify({
        "message": "updated"
    })
# ==========================
# RESOLVE
# ==========================

@alert_bp.patch("/alerts/<int:id>/resolve")
def resolve(id):

    alert = Alert.query.get_or_404(id)

    alert.is_resolved = True

    alert.status = "Resolved"

    db.session.commit()

    return jsonify({
        "message": "resolved"
    })
# ==========================
# DELETE
# ==========================

@alert_bp.delete("/alerts/<int:id>")
def delete(id):

    alert = Alert.query.get_or_404(id)

    db.session.delete(alert)

    db.session.commit()

    return jsonify({
        "message":"deleted"
    })