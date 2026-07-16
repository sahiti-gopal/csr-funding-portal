from flask import Blueprint, jsonify
from app.models.beneficiary_category import BeneficiaryCategory

beneficiary_category_bp = Blueprint(
    "beneficiary_categories",
    __name__
)


@beneficiary_category_bp.get("/beneficiary-categories")
def get_beneficiary_categories():

    categories = BeneficiaryCategory.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "icon": c.icon,
            "color": c.color,
            "is_active": c.is_active
        }
        for c in categories
    ])