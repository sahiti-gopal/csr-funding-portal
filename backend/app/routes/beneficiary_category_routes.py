from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.beneficiary_category import BeneficiaryCategory

beneficiary_category_bp = Blueprint(
    "beneficiary_categories",
    __name__
)


def _serialize(c):
    return {
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "icon": c.icon,
        "color": c.color,
        "is_active": c.is_active,
        "beneficiaries_total": sum(p.beneficiaries_reached or 0 for p in c.projects),
    }


@beneficiary_category_bp.get("/beneficiary-categories")
def get_beneficiary_categories():
    categories = BeneficiaryCategory.query.all()
    return jsonify([_serialize(c) for c in categories])


@beneficiary_category_bp.route("/beneficiary-categories", methods=["POST"])
def create_beneficiary_category():
    data = request.get_json()

    category = BeneficiaryCategory(
        name=data["name"],
        description=data.get("description"),
        icon=data.get("icon"),
        color=data.get("color"),
    )

    db.session.add(category)
    db.session.commit()

    return jsonify(_serialize(category)), 201


@beneficiary_category_bp.route("/beneficiary-categories/<int:id>", methods=["PUT"])
def update_beneficiary_category(id):
    data = request.get_json()
    category = BeneficiaryCategory.query.get_or_404(id)

    category.name = data["name"]
    category.description = data.get("description")

    db.session.commit()

    return jsonify(_serialize(category))


@beneficiary_category_bp.route("/beneficiary-categories/<int:id>", methods=["DELETE"])
def delete_beneficiary_category(id):
    category = BeneficiaryCategory.query.get_or_404(id)

    if category.projects:
        return jsonify(
            {"message": "Cannot delete a category that has projects assigned to it."}
        ), 409

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Beneficiary category deleted successfully"})
