import datetime

from flask import Blueprint, jsonify, request

from app.config import Config
from app.extensions import db
from app.models.donor import Donor
from app.models.project import Project
from app.models.report import Report

report_bp = Blueprint("reports", __name__)


def _fallback_target(achieved: int) -> int:
    if not achieved:
        return 0
    return max(achieved + 1, round(achieved * 1.25))


def _compute_report_stats(donor: Donor, financial_year: str) -> dict:
    projects = (
        Project.query.filter_by(donor_id=donor.id, financial_year=financial_year)
        .order_by(Project.project_name)
        .all()
    )

    outcome_progress = []
    for p in projects:
        achieved = p.beneficiaries_reached or 0
        target = _fallback_target(achieved)
        outcome_progress.append(
            {
                "programme": p.project_name,
                "location": p.location,
                "budget": float(p.budget or 0),
                "target": target,
                "achieved": achieved,
                "progress_pct": round(achieved / target * 100, 1) if target else 0,
            }
        )

    beneficiaries_total = sum(p.beneficiaries_reached or 0 for p in projects)
    committed = sum(float(p.budget or 0) for p in projects)
    received = sum(float(p.raised_amount or 0) for p in projects)
    utilized = sum(float(p.utilized_amount or 0) for p in projects)
    locations = sorted({p.location for p in projects if p.location})

    impact_highlights = {
        "beneficiaries_total": beneficiaries_total,
        "project_count": len(projects),
        "spend_efficiency_pct": round(utilized / received * 100, 1) if received else 0,
        "locations_covered": len(locations),
    }

    funds_summary = {
        "committed": committed,
        "received": received,
        "utilized": utilized,
        "balance": max(received - utilized, 0),
        "pending_receipt": max(committed - received, 0),
        "utilization_pct": round(utilized / received * 100, 1) if received else 0,
    }

    focus_area_totals = {}
    for p in projects:
        name = p.project_type.name if p.project_type else "Other"
        focus_area_totals[name] = focus_area_totals.get(name, 0) + (p.beneficiaries_reached or 0)

    impact_by_focus_area = [
        {
            "name": name,
            "beneficiaries": total,
            "pct": round(total / beneficiaries_total * 100, 1) if beneficiaries_total else 0,
        }
        for name, total in sorted(focus_area_totals.items(), key=lambda kv: kv[1], reverse=True)
    ]

    return {
        "donor": {"id": donor.id, "name": donor.name, "focus_area": donor.focus_area},
        "financial_year": financial_year,
        "outcome_progress": outcome_progress,
        "impact_highlights": impact_highlights,
        "funds_summary": funds_summary,
        "impact_by_focus_area": impact_by_focus_area,
        "locations": locations,
    }


def _generate_ai_narrative(stats: dict) -> str | None:
    if not Config.GEMINI_API_KEY:
        return None
    try:
        from google import genai
        from google.genai import types as genai_types
    except ImportError:
        return None

    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        system_prompt = (
            "You write a short, upbeat 2-3 sentence highlight summary for a "
            "corporate CSR annual report, for a non-technical audience. "
            "Use ONLY the numbers given below — never invent or estimate a "
            "number that isn't present. Do not mention SQL, databases, or "
            "JSON. Keep it to at most 3 sentences."
        )
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=f"Report data (JSON): {stats}",
            config=genai_types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=200,
                temperature=0.4,
            ),
        )
        return (response.text or "").strip() or None
    except Exception as exc:
        print(f"[reports] AI narrative failed (non-fatal): {exc}")
        return None


def _report_to_summary_dict(report: Report) -> dict:
    return {
        "id": report.id,
        "title": report.title,
        "donor": {"id": report.donor.id, "name": report.donor.name} if report.donor else None,
        "financial_year": report.financial_year,
        "generated_at": report.generated_at.isoformat() if report.generated_at else None,
        "review_status": report.review_status,
        "delivery_status": report.delivery_status,
    }


@report_bp.route("/reports", methods=["GET"])
def list_reports():
    reports = Report.query.order_by(Report.generated_at.desc()).all()
    return jsonify([_report_to_summary_dict(r) for r in reports])


@report_bp.route("/reports/preview", methods=["GET"])
def preview_report():
    donor_id = request.args.get("donor_id", type=int)
    financial_year = request.args.get("financial_year", type=str)

    if not donor_id or not financial_year:
        return jsonify({"error": "donor_id and financial_year are required"}), 400

    donor = Donor.query.get_or_404(donor_id)
    stats = _compute_report_stats(donor, financial_year)

    return jsonify(
        {
            "donor": stats["donor"],
            "financial_year": financial_year,
            "linked_projects": stats["impact_highlights"]["project_count"],
            "committed": stats["funds_summary"]["committed"],
        }
    )


def _generate_report(donor_id: int, financial_year: str) -> Report:
    donor = Donor.query.get_or_404(donor_id)

    report = Report.query.filter_by(donor_id=donor_id, financial_year=financial_year).first()
    if not report:
        report = Report(
            donor_id=donor_id,
            financial_year=financial_year,
            title=f"Annual CSR Report FY {financial_year}",
        )
        db.session.add(report)

    try:
        stats = _compute_report_stats(donor, financial_year)
        stats["ai_narrative"] = _generate_ai_narrative(stats)

        report.content = stats
        report.review_status = "Pending review"
        report.error_message = None
        report.generated_at = datetime.datetime.utcnow()
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        report = Report.query.filter_by(donor_id=donor_id, financial_year=financial_year).first()
        if not report:
            report = Report(
                donor_id=donor_id,
                financial_year=financial_year,
                title=f"Annual CSR Report FY {financial_year}",
            )
            db.session.add(report)
        report.review_status = "Failed"
        report.error_message = str(exc)
        report.generated_at = datetime.datetime.utcnow()
        db.session.commit()
        print(f"[reports] generation failed for donor={donor_id} fy={financial_year}: {exc}")

    return report


@report_bp.route("/reports", methods=["POST"])
def create_report():
    data = request.get_json(silent=True) or {}
    donor_id = data.get("donor_id")
    financial_year = data.get("financial_year")

    if not donor_id or not financial_year:
        return jsonify({"error": "donor_id and financial_year are required"}), 400

    report = _generate_report(int(donor_id), financial_year)
    return jsonify(_report_to_summary_dict(report)), 201


@report_bp.route("/reports/<int:report_id>", methods=["GET"])
def get_report(report_id):
    report = Report.query.get_or_404(report_id)
    return jsonify(
        {
            **_report_to_summary_dict(report),
            "content": report.content,
            "error_message": report.error_message,
        }
    )


@report_bp.route("/reports/<int:report_id>/retry", methods=["POST"])
def retry_report(report_id):
    report = Report.query.get_or_404(report_id)
    report = _generate_report(report.donor_id, report.financial_year)
    return jsonify(_report_to_summary_dict(report))


@report_bp.route("/reports/<int:report_id>/approve", methods=["POST"])
def approve_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.review_status == "Failed":
        return jsonify({"error": "Cannot approve a failed report. Retry generation first."}), 400
    report.review_status = "Approved"
    db.session.commit()
    return jsonify(_report_to_summary_dict(report))


@report_bp.route("/reports/<int:report_id>/deliver", methods=["POST"])
def deliver_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.review_status != "Approved":
        return jsonify({"error": "Only approved reports can be marked delivered."}), 400
    report.delivery_status = "Delivered"
    db.session.commit()
    return jsonify(_report_to_summary_dict(report))
