import os
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.donor import Donor
from app.models.donor_document import DonorDocument

document_bp = Blueprint("documents", __name__)

SEVERITY_RANK = {"Critical": 0, "Medium": 1, "Low": 2}


def _format_file_size(num_bytes):
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024


def _build_documents_payload(donor_id):
    documents = (
        DonorDocument.query.filter_by(donor_id=donor_id)
        .order_by(DonorDocument.id)
        .all()
    )

    required = len(documents)
    submitted = sum(1 for d in documents if d.status in ("Pending Review", "Verified"))
    pending = sum(1 for d in documents if d.status == "Pending Review")
    missing = sum(1 for d in documents if d.status in ("Missing", "Requested"))
    compliance = round(submitted / required * 100) if required else 0

    stats = {
        "required": required,
        "submitted": submitted,
        "pending": pending,
        "missing": missing,
        "compliance": compliance,
    }

    docs_payload = []
    for d in documents:
        payload = d.to_dict()
        payload["updated"] = (
            "Not Uploaded" if not d.uploaded_at else _relative_day(d.uploaded_at)
        )
        docs_payload.append(payload)

    categories_map = {}
    for d in documents:
        bucket = categories_map.setdefault(
            d.category, {"total": 0, "verified": 0}
        )
        bucket["total"] += 1
        if d.status == "Verified":
            bucket["verified"] += 1

    category_colors = {
        "Financial Documents": "#F97316",
        "Compliance Documents": "#7C3AED",
        "Legal Documents": "#2563EB",
        "Impact Reports": "#16A34A",
    }
    category_subtitles = {
        "Financial Documents": "Tax certificates and audit filings",
        "Compliance Documents": "Mandatory regulatory filings",
        "Legal Documents": "Agreements and registrations",
        "Impact Reports": "Quarterly and annual impact reports",
    }

    categories = []
    for name, bucket in categories_map.items():
        total = bucket["total"]
        verified = bucket["verified"]
        categories.append(
            {
                "title": name,
                "subtitle": category_subtitles.get(name, ""),
                "progress": round(verified / total * 100) if total else 0,
                "completed": f"{verified}/{total}",
                "color": category_colors.get(name, "#2563EB"),
            }
        )

    return stats, docs_payload, categories


def _relative_day(dt):
    days = (datetime.utcnow() - dt).days
    if days <= 0:
        return "Today"
    if days == 1:
        return "1 day ago"
    return f"{days} days ago"


def _build_recommendation(donor_id):
    missing_docs = (
        DonorDocument.query.filter_by(donor_id=donor_id, status="Missing")
        .all()
    )

    if not missing_docs:
        return "All required documents have been requested or submitted.", None

    missing_docs.sort(key=lambda d: SEVERITY_RANK.get(d.severity, 99))
    target = missing_docs[0]

    stats, _, _ = _build_documents_payload(donor_id)
    projected = min(100, stats["compliance"] + round(100 / max(stats["required"], 1)))

    text = (
        f"Request the donor's {target.title}. This will improve compliance "
        f"from {stats['compliance']}% to approximately {projected}%."
    )
    return text, target


@document_bp.route("/donors/<int:donor_id>/documents", methods=["GET"])
def get_donor_documents(donor_id):
    Donor.query.get_or_404(donor_id)

    stats, documents, categories = _build_documents_payload(donor_id)
    recommendation, _ = _build_recommendation(donor_id)

    return jsonify(
        {
            "stats": stats,
            "documents": documents,
            "categories": categories,
            "recommendation": recommendation,
        }
    )


@document_bp.route(
    "/donors/<int:donor_id>/documents/<int:doc_id>/upload", methods=["POST"]
)
def upload_donor_document(donor_id, doc_id):
    doc = DonorDocument.query.filter_by(id=doc_id, donor_id=donor_id).first_or_404()

    if "file" not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"message": "No file selected"}), 400

    upload_dir = os.path.join(
        current_app.config["UPLOAD_FOLDER"], "donor_documents", str(donor_id)
    )
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(f"{doc_id}_{file.filename}")
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    doc.file_path = file_path
    doc.file_size = _format_file_size(os.path.getsize(file_path))
    doc.status = "Pending Review"
    doc.owner = "You"
    doc.uploaded_at = datetime.utcnow()
    db.session.commit()

    stats, documents, categories = _build_documents_payload(donor_id)
    recommendation, _ = _build_recommendation(donor_id)
    return jsonify(
        {
            "stats": stats,
            "documents": documents,
            "categories": categories,
            "recommendation": recommendation,
        }
    )


@document_bp.route(
    "/donors/<int:donor_id>/documents/<int:doc_id>/review", methods=["POST"]
)
def review_donor_document(donor_id, doc_id):
    doc = DonorDocument.query.filter_by(id=doc_id, donor_id=donor_id).first_or_404()

    if doc.status == "Pending Review":
        doc.status = "Verified"
        db.session.commit()

    stats, documents, categories = _build_documents_payload(donor_id)
    recommendation, _ = _build_recommendation(donor_id)
    return jsonify(
        {
            "stats": stats,
            "documents": documents,
            "categories": categories,
            "recommendation": recommendation,
        }
    )


@document_bp.route(
    "/donors/<int:donor_id>/documents/generate-request", methods=["POST"]
)
def generate_document_request(donor_id):
    Donor.query.get_or_404(donor_id)

    recommendation, target = _build_recommendation(donor_id)
    if target is not None:
        target.status = "Requested"
        db.session.commit()

    stats, documents, categories = _build_documents_payload(donor_id)
    recommendation, _ = _build_recommendation(donor_id)
    return jsonify(
        {
            "stats": stats,
            "documents": documents,
            "categories": categories,
            "recommendation": recommendation,
        }
    )


@document_bp.route("/documents/<int:doc_id>/file", methods=["GET"])
def get_document_file(doc_id):
    doc = DonorDocument.query.get_or_404(doc_id)

    if not doc.file_path:
        return jsonify({"message": "No file uploaded for this document"}), 404

    directory, filename = os.path.split(doc.file_path)
    return send_from_directory(directory, filename)
