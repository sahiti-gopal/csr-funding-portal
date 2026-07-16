from flask import Blueprint, jsonify

from app.models.donor import Donor

donor_bp = Blueprint("donors", __name__)


@donor_bp.route("/donors", methods=["GET"])
def get_donors():
    donors = Donor.query.order_by(Donor.likelihood.desc()).all()

    return jsonify(
        [
            {
                "id": d.id,
                "name": d.name,
                "focus_area": d.focus_area,
                "likelihood": d.likelihood,
                "last_contact": (
                    str(d.last_contact) if d.last_contact else None
                ),
                "status": d.status,
            }
            for d in donors
        ]
    )
