import os
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request, send_from_directory

from sqlalchemy import func

from werkzeug.utils import secure_filename

from app.extensions import db

from app.models.donor import Donor
from app.models.project import Project

from app.models.donor_payment import DonorPayment
from app.models.payment_document import PaymentDocument


payments_bp = Blueprint(
    "payments",
    __name__,
)


def _format_file_size(num_bytes):
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024

@payments_bp.route(
    "/donors/<int:donor_id>/payments",
    methods=["GET"]
)
def get_donor_payments(donor_id):

    donor = Donor.query.get_or_404(donor_id)

    payments = (
        DonorPayment.query
        .filter_by(donor_id=donor_id)
        .order_by(
            DonorPayment.due_date.asc()
        )
        .all()
    )

    donor_projects = (
        Project.query
        .filter(Project.donor_id == donor_id)
        .all()
    )

    total_received = (
        db.session.query(
            func.coalesce(
                func.sum(
                    DonorPayment.amount
                ),
                0
            )
        )
        .filter(
            DonorPayment.donor_id == donor_id,
            DonorPayment.status == "Paid"
        )
        .scalar()
    )

    total_committed = sum(
        float(p.amount)
        for p in payments
    )

    pending_amount = (
        total_committed -
        float(total_received)
    )

    total_utilized = sum(
        float(p.utilized_amount or 0)
        for p in donor_projects
    )

    remaining_balance = (
        float(total_received)
        - total_utilized
    )
        # ----------------------------------------
    # KPI DATA
    # ----------------------------------------

    kpis = {
        "totalCommitted": total_committed,
        "totalReceived": float(total_received),
        "pendingDisbursement": pending_amount,
        "currentFYContribution": total_committed,
        "totalUtilized": total_utilized,
        "remainingBalance": remaining_balance,
    }

    # ----------------------------------------
    # TIMELINE
    # ----------------------------------------

    timeline = []

    for payment in payments:

        timeline.append({
            "id": payment.id,
            "title": payment.installment_name,
            "amount": float(payment.amount),
            "date": (
                payment.received_date.isoformat()
                if payment.received_date
                else payment.due_date.isoformat()
            ),
            "completed":
                payment.status == "Paid",
            "status":
                payment.status
        })

    # ----------------------------------------
    # PAYMENT SCHEDULE
    # ----------------------------------------

    schedule = []

    for payment in payments:

        schedule.append({

            "id":
                payment.id,

            "installment":
                payment.installment_name,

            "amount":
                float(payment.amount),

            "due":
                payment.due_date.isoformat()
                if payment.due_date else None,

            "received":
                payment.received_date.isoformat()
                if payment.received_date else None,

            "paymentMode":
                payment.payment_mode,

            "transactionId":
                payment.transaction_id,

            "status":
                payment.status,

            "remarks":
                payment.remarks

        })

    # ----------------------------------------
    # DOCUMENTS
    # ----------------------------------------

    documents = []

    for payment in payments:

        docs = []

        for document in payment.documents:

            docs.append({

                "id":
                    document.id,

                "name":
                    document.document_name,

                "type":
                    document.document_type,

                "url":
                    document.file_url,

                "size":
                    document.file_size,

                "status":
                    document.verification_status,

                "uploadedBy":
                    document.uploaded_by,

                "uploadedAt":
                    document.uploaded_at.isoformat()
                    if document.uploaded_at
                    else None

            })

        documents.append({

            "paymentId":
                payment.id,

            "installment":
                payment.installment_name,

            "amount":
                float(payment.amount),

            "receivedDate":
                payment.received_date.isoformat()
                if payment.received_date else None,

            "utr":
                payment.transaction_id,

            "documents":
                docs

            })
            # ----------------------------------------
    # LINKED PROJECTS / FUND UTILIZATION
    # ----------------------------------------

    projects = []

    for project in donor_projects:

        allocated = float(project.budget or 0)
        utilized = float(project.utilized_amount or 0)

        projects.append({

            "id":
                project.id,

            "projectId":
                project.id,

            "name":
                project.project_name,

            "location":
                project.location,

            "allocated":
                allocated,

            "utilized":
                utilized,

            "remaining":
                allocated - utilized,

            "progress":
                round(utilized / allocated * 100, 1)
                if allocated else 0

        })

    # ----------------------------------------
    # RECENT ACTIVITY (derived from payments/documents,
    # no separate activity-log table)
    # ----------------------------------------

    activity = []

    for payment in payments:

        if payment.status == "Paid" and payment.received_date:
            activity.append({
                "id": f"payment-{payment.id}",
                "title": f"Payment received: {payment.installment_name}",
                "type": "PAYMENT_RECEIVED",
                "icon": "bank",
                "date": payment.received_date.isoformat(),
            })
        elif payment.status == "Overdue":
            activity.append({
                "id": f"overdue-{payment.id}",
                "title": f"Payment overdue: {payment.installment_name}",
                "type": "PAYMENT_OVERDUE",
                "icon": "alert",
                "date": payment.due_date.isoformat() if payment.due_date else None,
            })
        elif payment.status == "Pending":
            activity.append({
                "id": f"pending-{payment.id}",
                "title": f"Payment pending: {payment.installment_name}",
                "type": "PAYMENT_PENDING",
                "icon": "clock",
                "date": payment.due_date.isoformat() if payment.due_date else None,
            })

        for document in payment.documents:
            activity.append({
                "id": f"doc-{document.id}",
                "title": f"Document uploaded: {document.document_name}",
                "type": (
                    "DOCUMENT_VERIFIED"
                    if document.verification_status == "Verified"
                    else "DOCUMENT_UPLOADED"
                ),
                "icon": (
                    "verified"
                    if document.verification_status == "Verified"
                    else "upload"
                ),
                "date": (
                    document.uploaded_at.isoformat()
                    if document.uploaded_at
                    else None
                ),
            })

    activity.sort(key=lambda a: a["date"] or "", reverse=True)
    activity = activity[:15]

    # ----------------------------------------
    # AI INSIGHTS
    # (no backing model anymore; kept as an empty list so the
    # frontend's existing empty-state rendering just applies)
    # ----------------------------------------

    ai_insights = []

    # ----------------------------------------
    # DONOR SUMMARY
    # ----------------------------------------

    donor_summary = {

        "id":
            donor.id,

        "name":
            donor.name,

        "organization":
            getattr(
                donor,
                "organization",
                donor.name
            ),

        "email":
            getattr(
                donor,
                "email",
                None
            ),

        "phone":
            getattr(
                donor,
                "phone",
                None
            ),

        "focusArea":
            getattr(
                donor,
                "focus_area",
                None
            ),

        "likelihood":
            getattr(
                donor,
                "likelihood",
                None
            )

    }
        # ----------------------------------------
    # FINAL RESPONSE
    # ----------------------------------------

    response = {

        "success": True,

        "donor": donor_summary,

        "kpis": kpis,

        "timeline": timeline,

        "schedule": schedule,

        "documents": documents,

        "projects": projects,

        "activity": activity,

        "aiInsights": ai_insights

    }

    return jsonify(response), 200


@payments_bp.route(
    "/payments/<int:payment_id>/documents",
    methods=["POST"],
)
def upload_payment_document(payment_id):
    payment = DonorPayment.query.get_or_404(payment_id)

    if "file" not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"message": "No file selected"}), 400

    document_type = request.form.get("document_type", "Other")

    upload_dir = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "payment_documents",
        str(payment_id),
    )
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    document = PaymentDocument(
        payment_id=payment.id,
        document_name=file.filename,
        document_type=document_type,
        file_size=_format_file_size(os.path.getsize(file_path)),
        verification_status="Pending",
        uploaded_by="You",
        uploaded_at=datetime.utcnow(),
    )
    db.session.add(document)
    db.session.flush()

    document.file_url = f"/api/payment-documents/{document.id}/file"
    document.file_path = file_path
    db.session.commit()

    return jsonify(document.to_dict()), 201


@payments_bp.route(
    "/payment-documents/<int:document_id>/file",
    methods=["GET"],
)
def get_payment_document_file(document_id):
    document = PaymentDocument.query.get_or_404(document_id)

    if not document.file_path:
        return jsonify({"message": "No file uploaded for this document"}), 404

    directory, filename = os.path.split(document.file_path)
    return send_from_directory(directory, filename)
