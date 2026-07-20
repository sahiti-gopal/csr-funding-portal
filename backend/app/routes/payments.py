from flask import Blueprint, jsonify

from sqlalchemy import func

from app.extensions import db

from app.models.donor import Donor
from app.models.project import Project

from app.models.donor_payment import DonorPayment


payments_bp = Blueprint(
    "payments",
    __name__,
)

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
