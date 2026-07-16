from flask import Blueprint, jsonify

from sqlalchemy import func

from app.extensions import db

from app.models.donor import Donor
from app.models.project import Project

from app.models.donor_payment import DonorPayment
from app.models.payment_document import PaymentDocument
from app.models.fund_allocation import FundAllocation
from app.models.payment_activity import PaymentActivity
from app.models.ai_payment_insight import AIPaymentInsight


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

    allocations = (
        FundAllocation.query
        .filter_by(donor_id=donor_id)
        .all()
    )

    activities = (
        PaymentActivity.query
        .filter_by(donor_id=donor_id)
        .order_by(
            PaymentActivity.activity_date.desc()
        )
        .limit(15)
        .all()
    )

    insights = (
        AIPaymentInsight.query
        .filter_by(donor_id=donor_id)
        .order_by(
            AIPaymentInsight.created_at.desc()
        )
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
        float(a.utilized_amount)
        for a in allocations
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

    for allocation in allocations:

        project = allocation.project

        projects.append({

            "id":
                allocation.id,

            "projectId":
                allocation.project_id,

            "name":
                project.name if project else "Unknown",

            "location":
                getattr(
                    project,
                    "location",
                    None
                ),

            "allocated":
                float(
                    allocation.allocated_amount
                ),

            "utilized":
                float(
                    allocation.utilized_amount
                ),

            "remaining":
                float(
                    allocation.remaining_amount
                ),

            "progress":
                allocation.utilization_percent()

        })

    # ----------------------------------------
    # RECENT ACTIVITY
    # ----------------------------------------

    activity = []

    for item in activities:

        activity.append({

    "id": item.id,

    "title": item.title,

    "type": item.activity_type,

    "icon": item.icon(),

    "date": (
        item.activity_date.isoformat()
        if item.activity_date
        else None
    )

})

    # ----------------------------------------
    # AI INSIGHTS
    # ----------------------------------------

    ai_insights = []

    for insight in insights:

        ai_insights.append({

    "id": insight.id,

    "title": insight.title,

    "description": insight.description,

    "priority": insight.priority,

    "priorityColor": insight.priority_color(),

    "createdAt": (
        insight.created_at.isoformat()
        if insight.created_at
        else None
    )

})

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