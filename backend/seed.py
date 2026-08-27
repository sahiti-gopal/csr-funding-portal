import os
import random
from datetime import date

from werkzeug.security import generate_password_hash

from app.config import Config
from app.extensions import db
from app.models import Role, ProjectType, BeneficiaryCategory, User
from app.models.project import Project
from app.models.project_metric import ProjectMetric
from app.models.project_location import ProjectLocation
from app.models.project_team_member import ProjectTeamMember
from app.models.project_document import ProjectDocument
from app.models.donor import Donor
from app.models.donor_payment import DonorPayment
from app.models.donor_document import DonorDocument
from app.models.risk import Risk
from app.models.alert import Alert
from app.models.report import Report
from app.routes.report_routes import _generate_report

DEMO_USERS = [
    {
        "first_name": os.getenv("SEED_ADMIN_FIRST_NAME", "CSR"),
        "last_name": os.getenv("SEED_ADMIN_LAST_NAME", "Admin"),
        "email": os.getenv("SEED_ADMIN_EMAIL", "admin@sevaimpact.org"),
        "password": os.getenv("SEED_ADMIN_PASSWORD", "Admin@123"),
        "role_name": "CSR Admin",
    },
]


def run_seed():
    # -----------------------------
    # Clear Existing Data
    # -----------------------------
    User.query.delete()
    Alert.query.delete()
    Report.query.delete()
    ProjectMetric.query.delete()
    ProjectLocation.query.delete()
    ProjectTeamMember.query.delete()
    ProjectDocument.query.delete()
    Risk.query.delete()
    Project.query.delete()
    DonorDocument.query.delete()
    DonorPayment.query.delete()
    Donor.query.delete()
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
    # Demo Users
    # -----------------------------
    for u in DEMO_USERS:
        role = Role.query.filter_by(name=u["role_name"]).first()
        db.session.add(
            User(
                first_name=u["first_name"],
                last_name=u["last_name"],
                email=u["email"],
                password_hash=generate_password_hash(u["password"]),
                role_id=role.id,
            )
        )
        print(f"created user: {u['email']} / {u['password']}")

    db.session.commit()

    # -----------------------------
    # Lookup Foreign Keys
    # -----------------------------
    education = ProjectType.query.filter_by(name="Education").first()
    healthcare = ProjectType.query.filter_by(name="Healthcare").first()
    environment = ProjectType.query.filter_by(name="Environment").first()
    women_emp = ProjectType.query.filter_by(name="Women Empowerment").first()
    livelihood = ProjectType.query.filter_by(name="Livelihood").first()
    rural_dev = ProjectType.query.filter_by(name="Rural Development").first()
    skill_dev = ProjectType.query.filter_by(name="Skill Development").first()

    students = BeneficiaryCategory.query.filter_by(name="Students").first()
    women = BeneficiaryCategory.query.filter_by(name="Women").first()
    children = BeneficiaryCategory.query.filter_by(name="Children").first()
    farmers = BeneficiaryCategory.query.filter_by(name="Farmers").first()
    youth = BeneficiaryCategory.query.filter_by(name="Youth").first()
    elderly = BeneficiaryCategory.query.filter_by(name="Elderly").first()

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
            logo_url="/images/logos/infosys-foundation.png",
        ),

        Donor(
            name="Tata Trusts",
            focus_area="Healthcare",
            status="Ready",
            likelihood=92,
            last_contact=date(2026, 7, 9),
            logo_url="/images/logos/tata-trusts.png",
        ),

        Donor(
            name="Reliance Foundation",
            focus_area="Rural Development",
            status="Interested",
            likelihood=90,
            last_contact=date(2026, 7, 8),
            logo_url="/images/logos/reliance-foundation.png",
        ),

        Donor(
            name="Wipro Cares",
            focus_area="Skill Development",
            status="Ready",
            likelihood=88,
            last_contact=date(2026, 7, 12),
            logo_url="/images/logos/wipro-cares.png",
        ),

        Donor(
            name="HCL Foundation",
            focus_area="Environment",
            status="Proposal Sent",
            likelihood=82,
            last_contact=date(2026, 7, 6),
            logo_url="/images/logos/hcl-foundation.png",
        ),

        Donor(
            name="Mahindra Rise",
            focus_area="Women Empowerment",
            status="Interested",
            likelihood=79,
            last_contact=date(2026, 7, 3),
            logo_url="/images/logos/mahindra-rise.png",
        ),

        Donor(
            name="Aditya Birla CSR",
            focus_area="Healthcare",
            status="Ready",
            likelihood=87,
            last_contact=date(2026, 7, 11),
            logo_url="/images/logos/aditya-birla-csr.png",
        ),

        Donor(
            name="JSW Foundation",
            focus_area="Education",
            status="Proposal Sent",
            likelihood=81,
            last_contact=date(2026, 7, 2),
            logo_url="/images/logos/jsw-foundation.png",
        ),

        Donor(
            name="Vedanta Foundation",
            focus_area="Environment",
            status="Negotiation",
            likelihood=76,
            last_contact=date(2026, 7, 5),
            logo_url="/images/logos/vedanta-foundation.png",
        ),

        Donor(
            name="SBI Foundation",
            focus_area="Livelihood",
            status="Ready",
            likelihood=89,
            last_contact=date(2026, 7, 13),
            logo_url="/images/logos/sbi-foundation.png",
        ),

        Donor(
            name="Axis Bank Foundation",
            focus_area="Education",
            status="Interested",
            likelihood=78,
            last_contact=date(2026, 7, 4),
            logo_url="/images/logos/axis-bank-foundation.png",
        ),

        Donor(
            name="L&T Public Charitable Trust",
            focus_area="Infrastructure",
            status="Ready",
            likelihood=91,
            last_contact=date(2026, 7, 14),
            logo_url="/images/logos/lt-public-charitable-trust.png",
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

    jsw = Donor.query.filter_by(
        name="JSW Foundation"
    ).first()

    aditya_birla = Donor.query.filter_by(
        name="Aditya Birla CSR"
    ).first()

    mahindra = Donor.query.filter_by(
        name="Mahindra Rise"
    ).first()

    hcl = Donor.query.filter_by(
        name="HCL Foundation"
    ).first()

    sbi = Donor.query.filter_by(
        name="SBI Foundation"
    ).first()

    vedanta = Donor.query.filter_by(
        name="Vedanta Foundation"
    ).first()

    axis = Donor.query.filter_by(
        name="Axis Bank Foundation"
    ).first()

    lt_trust = Donor.query.filter_by(
        name="L&T Public Charitable Trust"
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
            donor_id=infosys.id,
            raised_amount=500000,
            utilized_amount=420000,
            beneficiaries_reached=1800,
            metrics=[
                ProjectMetric(
                    icon="students",
                    title="Students Reached",
                    current_value=1800,
                    target_value=2500,
                ),
                ProjectMetric(
                    icon="schools",
                    title="Schools Covered",
                    current_value=12,
                    target_value=20,
                ),
                ProjectMetric(
                    icon="teachers",
                    title="Teachers Trained",
                    current_value=60,
                    target_value=100,
                ),
            ],
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
            donor_id=tata.id,
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
            donor_id=reliance.id,
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
            donor_id=wipro.id,
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
            donor_id=infosys.id,
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
            donor_id=tata.id,
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

        # ---------------------------------------------
        # Livelihood / Rural Development — rounds out the project-type
        # mix so the SDG Impact band reflects a fuller goal spread.
        # ---------------------------------------------

        Project(
            project_name="Farmer Livelihood Support",
            project_type_id=livelihood.id,
            beneficiary_category_id=farmers.id,
            budget=430000,
            location="Nagpur",
            region="West",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 4, 1),
            end_date=date(2026, 3, 31),
            donor_id=sbi.id,
            raised_amount=430000,
            utilized_amount=260000,
            beneficiaries_reached=810,
        ),

        Project(
            project_name="Rural Infrastructure Uplift",
            project_type_id=rural_dev.id,
            beneficiary_category_id=farmers.id,
            budget=520000,
            location="Nashik",
            region="West",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 5, 1),
            end_date=date(2026, 4, 30),
            donor_id=reliance.id,
            raised_amount=520000,
            utilized_amount=300000,
            beneficiaries_reached=1050,
        ),

        # ---------------------------------------------
        # Dummy data covering every Region x FY combo
        # ---------------------------------------------

        Project(
            project_name="Coastal School Renovation",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=380000,
            location="Chennai",
            region="South",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 6, 1),
            end_date=date(2024, 2, 28),
            donor_id=jsw.id,
            raised_amount=380000,
            utilized_amount=380000,
            beneficiaries_reached=1450,
        ),

        Project(
            project_name="Farmer Wellness Program",
            project_type_id=healthcare.id,
            beneficiary_category_id=women.id,
            budget=520000,
            location="Coimbatore",
            region="South",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 5, 1),
            end_date=date(2025, 1, 31),
            donor_id=aditya_birla.id,
            raised_amount=520000,
            utilized_amount=490000,
            beneficiaries_reached=1100,
        ),

        Project(
            project_name="Mumbai Slum Sanitation",
            project_type_id=healthcare.id,
            beneficiary_category_id=children.id,
            budget=610000,
            location="Mumbai",
            region="West",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 4, 1),
            end_date=date(2024, 3, 20),
            donor_id=mahindra.id,
            raised_amount=610000,
            utilized_amount=610000,
            beneficiaries_reached=2600,
        ),

        Project(
            project_name="Gujarat Green Belt",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=430000,
            location="Ahmedabad",
            region="West",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 6, 15),
            end_date=date(2025, 2, 10),
            donor_id=hcl.id,
            raised_amount=430000,
            utilized_amount=400000,
            beneficiaries_reached=1900,
        ),

        Project(
            project_name="Pune Women Cooperative",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=560000,
            location="Pune",
            region="West",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 6, 1),
            end_date=date(2026, 5, 31),
            donor_id=mahindra.id,
            raised_amount=560000,
            utilized_amount=310000,
            beneficiaries_reached=680,
        ),

        Project(
            project_name="Delhi Public School Kits",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=340000,
            location="New Delhi",
            region="North",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 7, 1),
            end_date=date(2024, 1, 15),
            donor_id=axis.id,
            raised_amount=340000,
            utilized_amount=340000,
            beneficiaries_reached=1600,
        ),

        Project(
            project_name="Punjab Farmer Support",
            project_type_id=healthcare.id,
            beneficiary_category_id=women.id,
            budget=470000,
            location="Ludhiana",
            region="North",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 4, 1),
            end_date=date(2025, 3, 1),
            donor_id=sbi.id,
            raised_amount=470000,
            utilized_amount=455000,
            beneficiaries_reached=980,
        ),

        Project(
            project_name="Himalayan Water Conservation",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=650000,
            location="Dehradun",
            region="North",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 5, 1),
            end_date=date(2026, 4, 30),
            donor_id=vedanta.id,
            raised_amount=650000,
            utilized_amount=380000,
            beneficiaries_reached=1200,
        ),

        Project(
            project_name="Haryana Skill Academy",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=720000,
            location="Gurugram",
            region="North",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 4, 1),
            end_date=date(2027, 3, 31),
            donor_id=wipro.id,
            raised_amount=720000,
            utilized_amount=90000,
            beneficiaries_reached=210,
        ),

        Project(
            project_name="Kolkata Literacy Mission",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=410000,
            location="Kolkata",
            region="East",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 5, 1),
            end_date=date(2024, 3, 31),
            donor_id=lt_trust.id,
            raised_amount=410000,
            utilized_amount=410000,
            beneficiaries_reached=1750,
        ),

        Project(
            project_name="Odisha Rural Health Camp",
            project_type_id=healthcare.id,
            beneficiary_category_id=children.id,
            budget=390000,
            location="Bhubaneswar",
            region="East",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 6, 1),
            end_date=date(2025, 2, 28),
            donor_id=tata.id,
            raised_amount=390000,
            utilized_amount=375000,
            beneficiaries_reached=1050,
        ),

        Project(
            project_name="Assam Tea Worker Welfare",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=480000,
            location="Guwahati",
            region="East",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 4, 1),
            end_date=date(2026, 3, 31),
            donor_id=reliance.id,
            raised_amount=480000,
            utilized_amount=260000,
            beneficiaries_reached=590,
        ),

        Project(
            project_name="Bihar Digital Inclusion",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=550000,
            location="Patna",
            region="East",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 5, 1),
            end_date=date(2027, 4, 30),
            donor_id=infosys.id,
            raised_amount=550000,
            utilized_amount=60000,
            beneficiaries_reached=140,
        ),

        # ---------------------------------------------
        # Extra data — one more project per Region x FY
        # so the Portfolio Overview filters show richer
        # results across every region/year combination.
        # ---------------------------------------------

        Project(
            project_name="Hyderabad STEM Labs",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=420000,
            location="Hyderabad",
            region="South",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 6, 15),
            end_date=date(2024, 3, 10),
            donor_id=jsw.id,
            raised_amount=420000,
            utilized_amount=420000,
            beneficiaries_reached=1320,
        ),

        Project(
            project_name="Andhra Maternal Care",
            project_type_id=healthcare.id,
            beneficiary_category_id=women.id,
            budget=560000,
            location="Visakhapatnam",
            region="South",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 5, 15),
            end_date=date(2025, 2, 20),
            donor_id=aditya_birla.id,
            raised_amount=560000,
            utilized_amount=540000,
            beneficiaries_reached=870,
        ),

        Project(
            project_name="Karnataka Women Weavers",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=610000,
            location="Mysore",
            region="South",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 5, 1),
            end_date=date(2026, 4, 30),
            donor_id=mahindra.id,
            raised_amount=610000,
            utilized_amount=350000,
            beneficiaries_reached=760,
        ),

        Project(
            project_name="Telangana Green Corridor",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=340000,
            location="Warangal",
            region="South",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 1, 31),
            donor_id=vedanta.id,
            raised_amount=340000,
            utilized_amount=40000,
            beneficiaries_reached=310,
        ),

        Project(
            project_name="Goa Coastal Cleanup",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=280000,
            location="Panaji",
            region="West",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 8, 1),
            end_date=date(2024, 1, 20),
            donor_id=hcl.id,
            raised_amount=280000,
            utilized_amount=280000,
            beneficiaries_reached=980,
        ),

        Project(
            project_name="Nagpur Child Health Drive",
            project_type_id=healthcare.id,
            beneficiary_category_id=children.id,
            budget=395000,
            location="Nagpur",
            region="West",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 7, 1),
            end_date=date(2025, 1, 15),
            donor_id=tata.id,
            raised_amount=395000,
            utilized_amount=380000,
            beneficiaries_reached=1420,
        ),

        Project(
            project_name="Surat Youth Skilling Hub",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=530000,
            location="Surat",
            region="West",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 7, 1),
            end_date=date(2026, 6, 30),
            donor_id=wipro.id,
            raised_amount=530000,
            utilized_amount=290000,
            beneficiaries_reached=640,
        ),

        Project(
            project_name="Nashik School Infrastructure",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=470000,
            location="Nashik",
            region="West",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 4, 15),
            end_date=date(2027, 2, 28),
            donor_id=axis.id,
            raised_amount=470000,
            utilized_amount=75000,
            beneficiaries_reached=260,
        ),

        Project(
            project_name="Jaipur Girls Education Drive",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=360000,
            location="Jaipur",
            region="North",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 9, 1),
            end_date=date(2024, 3, 15),
            donor_id=sbi.id,
            raised_amount=360000,
            utilized_amount=360000,
            beneficiaries_reached=1380,
        ),

        Project(
            project_name="Chandigarh Women Health Camp",
            project_type_id=healthcare.id,
            beneficiary_category_id=women.id,
            budget=410000,
            location="Chandigarh",
            region="North",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 8, 1),
            end_date=date(2025, 2, 15),
            donor_id=aditya_birla.id,
            raised_amount=410000,
            utilized_amount=395000,
            beneficiaries_reached=920,
        ),

        Project(
            project_name="Uttarakhand Forest Restoration",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=500000,
            location="Rishikesh",
            region="North",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 6, 1),
            end_date=date(2026, 5, 31),
            donor_id=hcl.id,
            raised_amount=500000,
            utilized_amount=270000,
            beneficiaries_reached=1050,
        ),

        Project(
            project_name="Lucknow Women Entrepreneurs",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=440000,
            location="Lucknow",
            region="North",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 5, 15),
            end_date=date(2027, 3, 31),
            donor_id=reliance.id,
            raised_amount=440000,
            utilized_amount=50000,
            beneficiaries_reached=180,
        ),

        Project(
            project_name="Jharkhand Tribal Education",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=370000,
            location="Ranchi",
            region="East",
            financial_year="2023-24",
            status="Completed",
            start_date=date(2023, 7, 15),
            end_date=date(2024, 2, 10),
            donor_id=lt_trust.id,
            raised_amount=370000,
            utilized_amount=370000,
            beneficiaries_reached=1240,
        ),

        Project(
            project_name="West Bengal Nutrition Program",
            project_type_id=healthcare.id,
            beneficiary_category_id=children.id,
            budget=400000,
            location="Kolkata",
            region="East",
            financial_year="2024-25",
            status="Completed",
            start_date=date(2024, 5, 20),
            end_date=date(2025, 1, 10),
            donor_id=tata.id,
            raised_amount=400000,
            utilized_amount=385000,
            beneficiaries_reached=1150,
        ),

        Project(
            project_name="Sikkim Eco Tourism Skilling",
            project_type_id=women_emp.id,
            beneficiary_category_id=women.id,
            budget=310000,
            location="Gangtok",
            region="East",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 6, 15),
            end_date=date(2026, 5, 15),
            donor_id=wipro.id,
            raised_amount=310000,
            utilized_amount=165000,
            beneficiaries_reached=420,
        ),

        Project(
            project_name="Odisha Coastal Afforestation",
            project_type_id=environment.id,
            beneficiary_category_id=children.id,
            budget=350000,
            location="Puri",
            region="East",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 6, 1),
            end_date=date(2027, 2, 28),
            donor_id=vedanta.id,
            raised_amount=350000,
            utilized_amount=45000,
            beneficiaries_reached=200,
        ),

    ]

    # ---------------------------------------------
    # Generated projects — bulk volume so aggregate/
    # group-by chat questions aren't trivially small,
    # plus deliberate coverage of every status value.
    # ---------------------------------------------

    NUM_GENERATED_PROJECTS = 55

    REGIONS = ["South", "West", "North", "East"]

    CITY_POOL = {
        "South": ["Hyderabad", "Bangalore", "Chennai", "Coimbatore", "Madurai", "Vijayawada", "Kochi", "Mysore", "Warangal", "Visakhapatnam"],
        "West": ["Mumbai", "Pune", "Nagpur", "Ahmedabad", "Surat", "Nashik", "Panaji", "Indore", "Rajkot", "Aurangabad"],
        "North": ["New Delhi", "Gurugram", "Chandigarh", "Lucknow", "Jaipur", "Dehradun", "Noida", "Kanpur", "Ludhiana", "Shimla"],
        "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi", "Gangtok", "Siliguri", "Cuttack", "Imphal", "Shillong"],
    }

    PROJECT_TYPE_VARS = {
        "Education": (education, students),
        "Healthcare": (healthcare, children),
        "Environment": (environment, children),
        "Women Empowerment": (women_emp, women),
        "Livelihood": (livelihood, farmers),
        "Rural Development": (rural_dev, farmers),
        "Skill Development": (skill_dev, youth),
    }

    THEMES_BY_TYPE = {
        "Education": ["School Renovation", "Digital Learning Lab", "Literacy Mission", "STEM Outreach", "Scholarship Program", "Teacher Training Initiative"],
        "Healthcare": ["Health Camp", "Maternal Care Program", "Nutrition Drive", "Sanitation Project", "Mobile Clinic Initiative", "Child Health Drive"],
        "Environment": ["Green Corridor", "Afforestation Drive", "Water Conservation Project", "Coastal Cleanup", "Solar Energy Initiative", "Waste Management Program"],
        "Women Empowerment": ["Women Cooperative", "Skill Academy", "Entrepreneurship Program", "Weavers Collective", "Self-Help Group Initiative"],
        "Livelihood": ["Farmer Livelihood Support", "Artisan Support Program", "Microfinance Initiative", "Livelihood Restoration Project"],
        "Rural Development": ["Rural Infrastructure Uplift", "Village Connectivity Project", "Rural Electrification Drive", "Community Center Initiative"],
        "Skill Development": ["Youth Skilling Hub", "Vocational Training Center", "Digital Skills Bootcamp", "Employment Readiness Program"],
    }

    DONOR_CYCLE = [infosys, tata, reliance, wipro, jsw, aditya_birla, mahindra, hcl, sbi, vedanta, axis, lt_trust]
    FINANCIAL_YEARS = ["2023-24", "2024-25", "2025-26", "2026-27"]
    FY_START_YEAR = {"2023-24": 2023, "2024-25": 2024, "2025-26": 2025, "2026-27": 2026}

    # Full status enum represented (existing hand-written projects only used
    # Active/Planning/Completed) — a real portfolio has stalled/dropped work too.
    STATUS_CYCLE = ["Active", "Planning", "Completed", "On Hold", "Cancelled", "Delayed"]

    UTILIZATION_RANGE_BY_STATUS = {
        "Completed": (95, 100),
        "Active": (30, 75),
        "Planning": (5, 20),
        "On Hold": (10, 40),
        "Cancelled": (0, 15),
        "Delayed": (15, 45),
    }

    rng = random.Random(42)  # deterministic across re-seeds
    type_names = list(PROJECT_TYPE_VARS.keys())
    generated_projects = []

    for i in range(NUM_GENERATED_PROJECTS):
        region = REGIONS[i % len(REGIONS)]
        type_name = type_names[i % len(type_names)]
        project_type, beneficiary = PROJECT_TYPE_VARS[type_name]
        fy = FINANCIAL_YEARS[i % len(FINANCIAL_YEARS)]
        status = STATUS_CYCLE[i % len(STATUS_CYCLE)]
        city = CITY_POOL[region][i % len(CITY_POOL[region])]
        theme = THEMES_BY_TYPE[type_name][i % len(THEMES_BY_TYPE[type_name])]
        donor = DONOR_CYCLE[i % len(DONOR_CYCLE)]

        budget = rng.randint(28, 95) * 10000
        util_min, util_max = UTILIZATION_RANGE_BY_STATUS[status]
        utilized_amount = round(budget * rng.randint(util_min, util_max) / 100)
        beneficiaries_reached = rng.randint(150, 2500)

        start_year = FY_START_YEAR[fy]
        start_date = date(start_year, ((i * 2) % 12) + 1, 1)
        end_date = date(start_year + 1, ((i * 3) % 12) + 1, 28)

        generated_projects.append(
            Project(
                project_name=f"{city} {theme}",
                project_type_id=project_type.id,
                beneficiary_category_id=beneficiary.id,
                budget=budget,
                location=city,
                region=region,
                financial_year=fy,
                status=status,
                start_date=start_date,
                end_date=end_date,
                donor_id=donor.id,
                raised_amount=budget,
                utilized_amount=utilized_amount,
                beneficiaries_reached=beneficiaries_reached,
            )
        )

    # ---------------------------------------------
    # Deliberate edge cases — hand-placed rather than
    # left to chance, so the chat/SQL pipeline is
    # guaranteed to see non-trivial relationships.
    # ---------------------------------------------

    edge_case_projects = [
        # Partial funding: raised < budget
        Project(
            project_name="Odisha Partial Funding Pilot",
            project_type_id=rural_dev.id,
            beneficiary_category_id=farmers.id,
            budget=800000,
            location="Cuttack",
            region="East",
            financial_year="2026-27",
            status="Active",
            start_date=date(2026, 2, 1),
            end_date=date(2027, 1, 31),
            donor_id=vedanta.id,
            raised_amount=500000,
            utilized_amount=210000,
            beneficiaries_reached=430,
        ),
        # Over-subscribed: raised > budget
        Project(
            project_name="Karnataka Oversubscribed Scholarship Fund",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=400000,
            location="Mysore",
            region="South",
            financial_year="2026-27",
            status="Active",
            start_date=date(2026, 3, 1),
            end_date=date(2027, 2, 28),
            donor_id=jsw.id,
            raised_amount=560000,
            utilized_amount=180000,
            beneficiaries_reached=610,
        ),
        # Zero utilization
        Project(
            project_name="Punjab Zero Utilization Health Initiative",
            project_type_id=healthcare.id,
            beneficiary_category_id=women.id,
            budget=450000,
            location="Ludhiana",
            region="North",
            financial_year="2026-27",
            status="Planning",
            start_date=date(2026, 8, 1),
            end_date=date(2027, 5, 31),
            donor_id=sbi.id,
            raised_amount=450000,
            utilized_amount=0,
            beneficiaries_reached=0,
        ),
        # Overdue: end_date already passed, still marked Active
        Project(
            project_name="Maharashtra Overdue Sanitation Drive",
            project_type_id=healthcare.id,
            beneficiary_category_id=children.id,
            budget=380000,
            location="Nagpur",
            region="West",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 6, 1),
            end_date=date(2026, 6, 1),
            donor_id=mahindra.id,
            raised_amount=380000,
            utilized_amount=190000,
            beneficiaries_reached=740,
        ),
        Project(
            project_name="Assam Overdue Literacy Drive",
            project_type_id=education.id,
            beneficiary_category_id=students.id,
            budget=310000,
            location="Guwahati",
            region="East",
            financial_year="2025-26",
            status="Active",
            start_date=date(2025, 4, 1),
            end_date=date(2026, 5, 15),
            donor_id=lt_trust.id,
            raised_amount=310000,
            utilized_amount=140000,
            beneficiaries_reached=520,
        ),
    ]

    projects = projects + generated_projects + edge_case_projects

    db.session.add_all(projects)

    db.session.commit()

    print(f"Projects inserted ({len(projects)} total).")

    # ===================================================
    # RISKS
    # ===================================================

    risks = [

        Risk(
            title="MOU verification pending",
            description="Rural Library Initiative's signed MOU failed an internal compliance check.",
            level="High",
            due_date=date(2026, 7, 18),
            action="Re-upload verified MOU",
            icon="shield",
        ),

        Risk(
            title="Quarterly report due",
            description="Q1 impact report submission deadline approaching for Tree Plantation Drive.",
            level="Medium",
            due_date=date(2026, 7, 20),
            action="Prepare report",
            icon="file",
        ),

        Risk(
            title="Utilization certificate overdue",
            description="Digital Classroom's UC has not been submitted to Infosys Foundation.",
            level="High",
            due_date=date(2026, 7, 25),
            action="Submit compliance document",
            icon="shield",
        ),

        Risk(
            title="Project deadline approaching",
            description="Village Health Camp ends in 6 weeks with utilization at just 55%.",
            level="High",
            due_date=date(2026, 8, 30),
            action="Review project timeline",
            icon="file",
        ),

        Risk(
            title="Low fund utilization",
            description="Women Skill Development has utilized only 60% of its budget with 8 months remaining.",
            level="Medium",
            due_date=date(2026, 9, 1),
            action="Accelerate spending plan",
            icon="check",
        ),

        Risk(
            title="Final settlement payment due",
            description="Infosys Foundation's final settlement for Digital Literacy Maharashtra is due next quarter.",
            level="Medium",
            due_date=date(2027, 3, 15),
            action="Send payment reminder",
            icon="file",
        ),

        # ---------------------------------------------
        # Additional risks — includes "Low" level, which
        # the hand-written set above never used, and
        # brings the table above trivial-group-by size.
        # ---------------------------------------------

        Risk(title="Minor documentation gap", description="Karnataka Women Weavers is missing a non-critical annexure in its proposal file.", level="Low", due_date=date(2026, 9, 10), action="Attach missing annexure", icon="file"),
        Risk(title="Vendor invoice mismatch", description="A vendor invoice for Rural Infrastructure Uplift doesn't match the approved PO amount.", level="Medium", due_date=date(2026, 9, 5), action="Reconcile invoice with PO", icon="file"),
        Risk(title="Site visit overdue", description="No field visit logged for Assam Tea Worker Welfare in over 90 days.", level="Medium", due_date=date(2026, 9, 12), action="Schedule field visit", icon="check"),
        Risk(title="Beneficiary count unverified", description="Reported beneficiary numbers for Bihar Digital Inclusion haven't been independently verified.", level="Low", due_date=date(2026, 9, 20), action="Commission third-party verification", icon="check"),
        Risk(title="Partial fund shortfall", description="Odisha Partial Funding Pilot has only received 62% of its approved budget.", level="High", due_date=date(2026, 9, 1), action="Follow up with donor on remaining tranche", icon="shield"),
        Risk(title="Over-subscription reconciliation", description="Karnataka Oversubscribed Scholarship Fund received more than its approved budget and needs reallocation sign-off.", level="Low", due_date=date(2026, 10, 1), action="Get reallocation approved", icon="check"),
        Risk(title="Zero spend flagged", description="Punjab Zero Utilization Health Initiative has not spent any of its raised funds since approval.", level="High", due_date=date(2026, 9, 15), action="Confirm project start plan", icon="shield"),
        Risk(title="Project overdue for closure", description="Maharashtra Overdue Sanitation Drive is past its end date but still marked Active.", level="High", due_date=date(2026, 9, 3), action="Close out or extend project timeline", icon="shield"),
        Risk(title="Project overdue for closure", description="Assam Overdue Literacy Drive is past its end date but still marked Active.", level="High", due_date=date(2026, 9, 8), action="Close out or extend project timeline", icon="shield"),
        Risk(title="Staffing gap reported", description="Haryana Skill Academy's field coordinator role has been vacant for a month.", level="Medium", due_date=date(2026, 9, 18), action="Fill field coordinator vacancy", icon="check"),
        Risk(title="Data quality flag", description="Duplicate beneficiary entries detected in Odisha Rural Health Camp's tracker.", level="Low", due_date=date(2026, 9, 25), action="Deduplicate beneficiary records", icon="file"),
        Risk(title="Communication lapse", description="No status update sent to Vedanta Foundation for Telangana Green Corridor in over 60 days.", level="Medium", due_date=date(2026, 9, 22), action="Send donor status update", icon="file"),
        Risk(title="Renewal decision pending", description="Surat Youth Skilling Hub's donor renewal decision is pending beyond the usual review window.", level="Medium", due_date=date(2026, 10, 5), action="Follow up on renewal decision", icon="check"),
        Risk(title="Minor budget variance", description="Nashik School Infrastructure shows a small unexplained variance between planning and actual budget.", level="Low", due_date=date(2026, 10, 10), action="Reconcile budget variance", icon="file"),
        Risk(title="Permit renewal required", description="Gujarat Green Belt's local environmental permit is due for renewal.", level="Medium", due_date=date(2026, 10, 15), action="Renew environmental permit", icon="shield"),
        Risk(title="Training completion lag", description="Haryana Skill Academy is behind its planned training-session schedule.", level="Low", due_date=date(2026, 10, 20), action="Catch up on training schedule", icon="check"),
        Risk(title="Insurance coverage gap", description="Uttarakhand Forest Restoration's field team insurance coverage lapsed last month.", level="High", due_date=date(2026, 9, 6), action="Renew field team insurance", icon="shield"),
        Risk(title="Photo documentation missing", description="Sikkim Eco Tourism Skilling is missing required photo documentation for its last milestone.", level="Low", due_date=date(2026, 10, 25), action="Upload milestone photo documentation", icon="file"),

    ]

    db.session.add_all(risks)

    db.session.commit()

    print(f"Risks inserted ({len(risks)} total).")

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

    # ===================================================
    # DONOR DOCUMENTS (compliance checklist per donor)
    # ===================================================

    DOCUMENT_TEMPLATE = [
        ("Financial Documents", "Audited Financial Statement", "Medium", "Verified", date(2026, 4, 15)),
        ("Financial Documents", "Tax Exemption Certificate", "Medium", "Verified", date(2026, 4, 15)),
        ("Financial Documents", "CSR Fund Utilization Report", "Medium", "Verified", date(2026, 7, 15)),
        ("Financial Documents", "Annual Report", "Medium", "Pending Review", date(2026, 7, 15)),

        ("Compliance Documents", "CSR-1 Registration", "Critical", "Missing", None),
        ("Compliance Documents", "80G Certificate", "Critical", "Missing", None),
        ("Compliance Documents", "12A Registration", "Medium", "Pending Review", date(2026, 6, 30)),
        ("Compliance Documents", "FCRA Registration", "Low", "Verified", date(2026, 3, 1)),

        ("Legal Documents", "MOU Agreement", "Medium", "Verified", date(2026, 2, 1)),
        ("Legal Documents", "Trust Deed", "Low", "Verified", date(2026, 1, 1)),
        ("Legal Documents", "Board Resolution", "Medium", "Verified", date(2026, 5, 1)),
        ("Legal Documents", "Registration Certificate", "Low", "Missing", None),

        ("Impact Reports", "Q1 Impact Report", "Medium", "Verified", date(2026, 4, 30)),
        ("Impact Reports", "Q2 Impact Report", "Medium", "Verified", date(2026, 7, 31)),
        ("Impact Reports", "Q3 Impact Report", "Medium", "Pending Review", date(2026, 10, 31)),
        ("Impact Reports", "Annual Impact Report", "Medium", "Missing", date(2027, 3, 31)),
    ]

    seed_uploads_dir = os.path.join(
        Config.UPLOAD_FOLDER, "donor_documents", "seed"
    )
    os.makedirs(seed_uploads_dir, exist_ok=True)

    donor_documents = []

    for donor in donors:
        for category, title, severity, status, due_date in DOCUMENT_TEMPLATE:
            has_file = status in ("Pending Review", "Verified")

            file_path = None
            if has_file:
                safe_title = title.lower().replace(" ", "_").replace("-", "_")
                file_path = os.path.join(
                    seed_uploads_dir, f"{donor.id}_{safe_title}.pdf"
                )
                if not os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        f.write(f"Placeholder document: {title}\n")

            donor_documents.append(
                DonorDocument(
                    donor_id=donor.id,
                    category=category,
                    title=title,
                    due_date=due_date,
                    severity=severity,
                    status=status,
                    owner="Meera" if has_file else None,
                    uploaded_at=due_date if has_file else None,
                    file_path=file_path,
                    file_size="182 KB" if has_file else None,
                )
            )

    db.session.add_all(donor_documents)

    db.session.commit()

    print("Donor documents inserted.")

    print("Payments inserted.")

    # ===================================================
    # REPORTS (real generation, seeded into a few review states)
    # ===================================================

    tata = Donor.query.filter_by(name="Tata Trusts").first()
    infosys = Donor.query.filter_by(name="Infosys Foundation").first()
    hcl = Donor.query.filter_by(name="HCL Foundation").first()

    approved_report = _generate_report(tata.id, "2024-25")
    approved_report.review_status = "Approved"
    approved_report.delivery_status = "Delivered"

    pending_report = _generate_report(infosys.id, "2026-27")
    pending_report.review_status = "Pending review"
    pending_report.delivery_status = "Awaiting"

    db.session.commit()

    failed_report = Report(
        donor_id=hcl.id,
        financial_year="2024-25",
        title="Annual CSR Report FY 2024-25",
        review_status="Failed",
        delivery_status="Awaiting",
        error_message="Generation timed out while summarizing linked projects.",
    )
    db.session.add(failed_report)
    db.session.commit()

    print("Reports inserted.")

    # -----------------------------
    # Alerts
    # -----------------------------
    def project(name):
        return Project.query.filter_by(project_name=name).first()

    digital = project("Digital Classroom")
    health = project("Village Health Camp")
    tree = project("Tree Plantation Drive")
    skill = project("Women Skill Development")
    library = project("Rural Library Initiative")

    alerts = [
        Alert(
            title="Donor payment overdue",
            description="Tata Trusts' final installment is overdue for Village Health Camp.",
            category="DONOR RISK",
            priority="HIGH",
            status="Unread",
            due_date=date(2026, 8, 1),
            is_read=False,
            is_resolved=False,
            project_id=health.id if health else None,
        ),
        Alert(
            title="Missing compliance document",
            description="Utilization certificate pending upload for Digital Classroom.",
            category="DOCUMENTS",
            priority="MEDIUM",
            status="Unread",
            due_date=date(2026, 7, 25),
            is_read=False,
            is_resolved=False,
            project_id=digital.id if digital else None,
        ),
        Alert(
            title="Quarterly report due",
            description="Q1 impact report submission deadline approaching for Tree Plantation Drive.",
            category="REPORTS",
            priority="MEDIUM",
            status="Unread",
            due_date=date(2026, 7, 20),
            is_read=False,
            is_resolved=False,
            project_id=tree.id if tree else None,
        ),
        Alert(
            title="Budget utilization low",
            description="Women Skill Development has utilized less than 50% of allocated budget.",
            category="DONOR RISK",
            priority="LOW",
            status="Read",
            due_date=date(2026, 9, 1),
            is_read=True,
            is_resolved=False,
            project_id=skill.id if skill else None,
        ),
        Alert(
            title="System maintenance scheduled",
            description="Portal will undergo scheduled maintenance this weekend.",
            category="SYSTEM",
            priority="LOW",
            status="Read",
            due_date=None,
            is_read=True,
            is_resolved=True,
            project_id=None,
        ),
        Alert(
            title="Document verification failed",
            description="Uploaded MOU for Rural Library Initiative failed verification checks.",
            category="DOCUMENTS",
            priority="HIGH",
            status="Unread",
            due_date=date(2026, 7, 18),
            is_read=False,
            is_resolved=False,
            project_id=library.id if library else None,
        ),
    ]

    # ---------------------------------------------
    # Additional alerts — brings the table above
    # trivial-group-by size and covers HIGH/MEDIUM/LOW
    # priority with a realistic mix of read/unread.
    # ---------------------------------------------

    overdue1 = project("Maharashtra Overdue Sanitation Drive")
    overdue2 = project("Assam Overdue Literacy Drive")
    zero_util = project("Punjab Zero Utilization Health Initiative")
    partial = project("Odisha Partial Funding Pilot")
    oversub = project("Karnataka Oversubscribed Scholarship Fund")

    extra_alerts = [
        Alert(title="Project past end date", description="Maharashtra Overdue Sanitation Drive is past its end date but still marked Active.", category="DONOR RISK", priority="HIGH", status="Unread", due_date=date(2026, 9, 3), is_read=False, is_resolved=False, project_id=overdue1.id if overdue1 else None),
        Alert(title="Project past end date", description="Assam Overdue Literacy Drive is past its end date but still marked Active.", category="DONOR RISK", priority="HIGH", status="Unread", due_date=date(2026, 9, 8), is_read=False, is_resolved=False, project_id=overdue2.id if overdue2 else None),
        Alert(title="Zero utilization detected", description="Punjab Zero Utilization Health Initiative has not spent any raised funds.", category="DONOR RISK", priority="HIGH", status="Unread", due_date=date(2026, 9, 15), is_read=False, is_resolved=False, project_id=zero_util.id if zero_util else None),
        Alert(title="Funding shortfall", description="Odisha Partial Funding Pilot has only received 62% of its approved budget.", category="DONOR RISK", priority="MEDIUM", status="Unread", due_date=date(2026, 9, 1), is_read=False, is_resolved=False, project_id=partial.id if partial else None),
        Alert(title="Reallocation approval needed", description="Karnataka Oversubscribed Scholarship Fund exceeded its approved budget and needs reallocation sign-off.", category="DONOR RISK", priority="LOW", status="Read", due_date=date(2026, 10, 1), is_read=True, is_resolved=False, project_id=oversub.id if oversub else None),
        Alert(title="Document verification failed", description="Compliance document verification failed for a recent upload.", category="DOCUMENTS", priority="MEDIUM", status="Unread", due_date=date(2026, 9, 20), is_read=False, is_resolved=False, project_id=None),
        Alert(title="Report submission delayed", description="Quarterly impact report submission slipped past its due date.", category="REPORTS", priority="MEDIUM", status="Read", due_date=date(2026, 8, 30), is_read=True, is_resolved=False, project_id=None),
        Alert(title="Donor renewal pending", description="A donor renewal decision is pending beyond the usual review window.", category="DONOR RISK", priority="LOW", status="Read", due_date=date(2026, 10, 5), is_read=True, is_resolved=False, project_id=None),
        Alert(title="Field visit overdue", description="No field visit logged for a project in over 90 days.", category="DONOR RISK", priority="MEDIUM", status="Unread", due_date=date(2026, 9, 12), is_read=False, is_resolved=False, project_id=None),
        Alert(title="Data quality flag", description="Duplicate beneficiary entries detected in a project tracker.", category="DOCUMENTS", priority="LOW", status="Read", due_date=date(2026, 9, 25), is_read=True, is_resolved=True, project_id=None),
        Alert(title="Insurance coverage lapsed", description="Field team insurance coverage lapsed for an active project.", category="DONOR RISK", priority="HIGH", status="Unread", due_date=date(2026, 9, 6), is_read=False, is_resolved=False, project_id=None),
        Alert(title="Permit renewal required", description="A local environmental permit is due for renewal.", category="DOCUMENTS", priority="MEDIUM", status="Unread", due_date=date(2026, 10, 15), is_read=False, is_resolved=False, project_id=None),
        Alert(title="Training schedule slipping", description="A skilling program is behind its planned training-session schedule.", category="DONOR RISK", priority="LOW", status="Read", due_date=date(2026, 10, 20), is_read=True, is_resolved=False, project_id=None),
        Alert(title="System maintenance completed", description="Scheduled portal maintenance completed successfully.", category="SYSTEM", priority="LOW", status="Read", due_date=None, is_read=True, is_resolved=True, project_id=None),
        Alert(title="New donor onboarded", description="A new donor record was added to the portal.", category="SYSTEM", priority="LOW", status="Read", due_date=None, is_read=True, is_resolved=True, project_id=None),
        Alert(title="Budget variance flagged", description="A small unexplained variance was found between planning and actual budget.", category="DONOR RISK", priority="LOW", status="Unread", due_date=date(2026, 10, 10), is_read=False, is_resolved=False, project_id=None),
        Alert(title="Photo documentation missing", description="Required milestone photo documentation is missing for a project.", category="DOCUMENTS", priority="LOW", status="Unread", due_date=date(2026, 10, 25), is_read=False, is_resolved=False, project_id=None),
        Alert(title="Staffing gap reported", description="A field coordinator role has been vacant for a month on an active project.", category="DONOR RISK", priority="MEDIUM", status="Unread", due_date=date(2026, 9, 18), is_read=False, is_resolved=False, project_id=None),
    ]

    alerts = alerts + extra_alerts

    db.session.add_all(alerts)
    db.session.commit()

    print(f"Inserted {len(alerts)} alerts.")

    print("Database seeded successfully!")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        run_seed()