from datetime import date

from app import create_app
from app.extensions import db
from app.models import Role, ProjectType, BeneficiaryCategory
from app.models.project import Project
from app.models.project_metric import ProjectMetric
from app.models.project_location import ProjectLocation
from app.models.project_team_member import ProjectTeamMember
from app.models.project_document import ProjectDocument
from app.models.donor import Donor
from app.models.donor_payment import DonorPayment
from app.models.risk import Risk
from app.models.alert import Alert

app = create_app()

with app.app_context():

    # -----------------------------
    # Clear Existing Data
    # -----------------------------
    Alert.query.delete()
    ProjectMetric.query.delete()
    ProjectLocation.query.delete()
    ProjectTeamMember.query.delete()
    ProjectDocument.query.delete()
    Project.query.delete()
    Donor.query.delete()
    Risk.query.delete()
    BeneficiaryCategory.query.delete()
    ProjectType.query.delete()
    Role.query.delete()

    db.session.commit()

    # -----------------------------
    # Roles
    # -----------------------------
    roles = [
        "CSR Admin",
        "Project Manager",
        "Finance Manager",
        "Field Officer",
        "Auditor",
    ]

    for role in roles:
        db.session.add(
            Role(
                name=role,
                description=f"{role} Role",
            )
        )

    # -----------------------------
    # Project Types
    # -----------------------------
    project_types = [
        "Education",
        "Healthcare",
        "Environment",
        "Women Empowerment",
        "Livelihood",
        "Skill Development",
        "Rural Development",
    ]

    for pt in project_types:
        db.session.add(ProjectType(name=pt))

    # -----------------------------
    # Beneficiary Categories
    # -----------------------------
    beneficiaries = [
        "Students",
        "Women",
        "Children",
        "Farmers",
        "Youth",
        "Elderly",
    ]

    for b in beneficiaries:
        db.session.add(BeneficiaryCategory(name=b))

    db.session.commit()

    # -----------------------------
    # Lookup Foreign Keys
    # -----------------------------
    education = ProjectType.query.filter_by(name="Education").first()
    healthcare = ProjectType.query.filter_by(name="Healthcare").first()
    environment = ProjectType.query.filter_by(name="Environment").first()
    women_emp = ProjectType.query.filter_by(name="Women Empowerment").first()

    students = BeneficiaryCategory.query.filter_by(name="Students").first()
    women = BeneficiaryCategory.query.filter_by(name="Women").first()
    children = BeneficiaryCategory.query.filter_by(name="Children").first()

    # ===================================================
    # DONORS
    # ===================================================

    donors = [

        Donor(
            name="Infosys Foundation",
            focus_area="Education",
            status="Ready",
            likelihood=95,
            last_contact=date(2026, 7, 10),
        ),

        Donor(
            name="Tata Trusts",
            focus_area="Healthcare",
            status="Ready",
            likelihood=92,
            last_contact=date(2026, 7, 9),
        ),

        Donor(
            name="Reliance Foundation",
            focus_area="Rural Development",
            status="Interested",
            likelihood=90,
            last_contact=date(2026, 7, 8),
        ),

        Donor(
            name="Wipro Cares",
            focus_area="Skill Development",
            status="Ready",
            likelihood=88,
            last_contact=date(2026, 7, 12),
        ),

        Donor(
            name="HCL Foundation",
            focus_area="Environment",
            status="Proposal Sent",
            likelihood=82,
            last_contact=date(2026, 7, 6),
        ),

        Donor(
            name="Mahindra Rise",
            focus_area="Women Empowerment",
            status="Interested",
            likelihood=79,
            last_contact=date(2026, 7, 3),
        ),

        Donor(
            name="Aditya Birla CSR",
            focus_area="Healthcare",
            status="Ready",
            likelihood=87,
            last_contact=date(2026, 7, 11),
        ),

        Donor(
            name="JSW Foundation",
            focus_area="Education",
            status="Proposal Sent",
            likelihood=81,
            last_contact=date(2026, 7, 2),
        ),

        Donor(
            name="Vedanta Foundation",
            focus_area="Environment",
            status="Negotiation",
            likelihood=76,
            last_contact=date(2026, 7, 5),
        ),

        Donor(
            name="SBI Foundation",
            focus_area="Livelihood",
            status="Ready",
            likelihood=89,
            last_contact=date(2026, 7, 13),
        ),

        Donor(
            name="Axis Bank Foundation",
            focus_area="Education",
            status="Interested",
            likelihood=78,
            last_contact=date(2026, 7, 4),
        ),

        Donor(
            name="L&T Public Charitable Trust",
            focus_area="Infrastructure",
            status="Ready",
            likelihood=91,
            last_contact=date(2026, 7, 14),
        ),

    ]

    db.session.add_all(donors)

    db.session.commit()

    print("Donors inserted.")

    # ===================================================
    # PROJECTS
    # ===================================================

    infosys = Donor.query.filter_by(
        name="Infosys Foundation"
    ).first()

    tata = Donor.query.filter_by(
        name="Tata Trusts"
    ).first()

    reliance = Donor.query.filter_by(
        name="Reliance Foundation"
    ).first()

    wipro = Donor.query.filter_by(
        name="Wipro Cares"
    ).first()

    projects = [

        Project(
            project_name="Digital Classroom",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=500000,
            location="Hyderabad",
            region="South",
            financial_year="2026-27",
            status="Active",
            start_date=date(2026, 1, 15),
            end_date=date(2026, 12, 31),
            sponsor_name="Infosys Foundation",
            sponsor_sector="Education",
            raised_amount=500000,
            utilized_amount=420000,
            beneficiaries_reached=1800,
        ),

        Project(
            project_name="Village Health Camp",
            project_type_id=healthcare.id,
            beneficiary_category_id=women.id,
            budget=750000,
            location="Warangal",
            region="South",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 8, 30),
            sponsor_name="Tata Trusts",
            sponsor_sector="Healthcare",
            raised_amount=750000,
            utilized_amount=410000,
            beneficiaries_reached=950,
        ),

        Project(
            project_name="Tree Plantation Drive",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=300000,
            location="Vijayawada",
            region="South",
            financial_year="2025-26",
            status="Completed",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 10, 1),
            sponsor_name="Reliance Foundation",
            sponsor_sector="Environment",
            raised_amount=300000,
            utilized_amount=300000,
            beneficiaries_reached=2400,
        ),

        Project(
            project_name="Women Skill Development",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=900000,
            location="Bangalore",
            region="South",
            financial_year="2026-27",
            status="Active",
            start_date=date(2026, 3, 1),
            end_date=date(2027, 3, 1),
            sponsor_name="Wipro Cares",
            sponsor_sector="Skill Development",
            raised_amount=900000,
            utilized_amount=540000,
            beneficiaries_reached=720,
        ),

        Project(
            project_name="Rural Library Initiative",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=450000,
            location="Kurnool",
            region="South",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 5, 10),
            end_date=date(2026, 11, 30),
            sponsor_name="Infosys Foundation",
            sponsor_sector="Education",
            raised_amount=450000,
            utilized_amount=180000,
            beneficiaries_reached=640,
        ),

        # ---------------------------------------------
        # Detailed project (drives the Project Details page)
        # ---------------------------------------------
        Project(
            project_name="Digital Literacy Maharashtra",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=1200000,
            location="Maharashtra",
            region="West",
            financial_year="2026-27",
            status="Active",
            start_date=date(2026, 1, 10),
            end_date=date(2026, 12, 20),
            sponsor_name="Tata Trusts",
            sponsor_sector="Education",
            raised_amount=1200000,
            utilized_amount=980000,
            beneficiaries_reached=12000,
            metrics=[
                ProjectMetric(
                    icon="students",
                    title="Students Reached",
                    current_value=12000,
                    target_value=15000,
                ),
                ProjectMetric(
                    icon="schools",
                    title="Schools Covered",
                    current_value=48,
                    target_value=60,
                ),
                ProjectMetric(
                    icon="teachers",
                    title="Teachers Trained",
                    current_value=390,
                    target_value=600,
                ),
            ],
            locations=[
                ProjectLocation(name="Pune"),
                ProjectLocation(name="Nashik"),
                ProjectLocation(name="Aurangabad"),
            ],
            team_members=[
                ProjectTeamMember(
                    name="Priya Sharma",
                    role="Project Manager",
                    tag="Lead",
                ),
                ProjectTeamMember(
                    name="Rohan Mehta",
                    role="Field Coordinator",
                    tag="Ops",
                ),
                ProjectTeamMember(
                    name="Anita Desai",
                    role="Training Lead",
                    tag="Training",
                ),
                ProjectTeamMember(
                    name="Tata Trusts",
                    role="CSR Sponsor",
                    tag="Partner",
                ),
            ],
            documents=[
                ProjectDocument(name="Project Proposal.pdf", size="2.4 MB"),
                ProjectDocument(name="Q2 Impact Report.pdf", size="1.1 MB"),
                ProjectDocument(name="Budget Breakdown.xlsx", size="820 KB"),
            ],
        ),

    ]

    db.session.add_all(projects)

    db.session.commit()

    print("Projects inserted.")

    # ===================================================
    # PAYMENT DATA
    # ===================================================

    infosys = Donor.query.filter_by(
        name="Infosys Foundation"
    ).first()

    tata = Donor.query.filter_by(
        name="Tata Trusts"
    ).first()

    reliance = Donor.query.filter_by(
        name="Reliance Foundation"
    ).first()

    wipro = Donor.query.filter_by(
        name="Wipro Cares"
    ).first()

    digital = Project.query.filter_by(
        project_name="Digital Classroom"
    ).first()

    health = Project.query.filter_by(
        project_name="Village Health Camp"
    ).first()

    tree = Project.query.filter_by(
        project_name="Tree Plantation Drive"
    ).first()

    skill = Project.query.filter_by(
        project_name="Women Skill Development"
    ).first()

    library = Project.query.filter_by(
        project_name="Rural Library Initiative"
    ).first()

    literacy = Project.query.filter_by(
        project_name="Digital Literacy Maharashtra"
    ).first()

    payments = [

        DonorPayment(
            donor_id=infosys.id,
            installment_name="Installment 1",
            amount=8500000,
            due_date=date(2026, 4, 30),
            received_date=date(2026, 4, 28),
            payment_mode="NEFT",
            transaction_id="INF260428001",
            status="Paid",
            remarks="Received"
        ),

        DonorPayment(
            donor_id=infosys.id,
            installment_name="Installment 2",
            amount=8500000,
            due_date=date(2026, 8, 15),
            received_date=date(2026, 8, 14),
            payment_mode="RTGS",
            transaction_id="INF260814002",
            status="Paid",
            remarks="Received"
        ),

        DonorPayment(
            donor_id=infosys.id,
            installment_name="Final Settlement",
            amount=3100000,
            due_date=date(2027, 3, 15),
            payment_mode="Pending",
            transaction_id="",
            status="Pending",
            remarks="Awaiting"
        ),

        DonorPayment(
            donor_id=tata.id,
            installment_name="Installment 1",
            amount=12000000,
            due_date=date(2026, 3, 25),
            received_date=date(2026, 3, 23),
            payment_mode="RTGS",
            transaction_id="TATA260323001",
            status="Paid",
            remarks="Received"
        ),

        DonorPayment(
            donor_id=reliance.id,
            installment_name="Installment 1",
            amount=6000000,
            due_date=date(2026, 5, 10),
            received_date=date(2026, 5, 9),
            payment_mode="NEFT",
            transaction_id="REL260509001",
            status="Paid",
            remarks="Received"
        ),

        DonorPayment(
            donor_id=wipro.id,
            installment_name="Installment 1",
            amount=9000000,
            due_date=date(2026, 2, 18),
            received_date=date(2026, 2, 16),
            payment_mode="IMPS",
            transaction_id="WIP260216001",
            status="Paid",
            remarks="Received"
        ),

    ]

    db.session.add_all(payments)

    db.session.commit()

    print("Payments inserted.")

    print("Database seeded successfully!")