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
from app.models.report import Report
from app.routes.report_routes import _generate_report

app = create_app()

with app.app_context():

    # -----------------------------
    # Clear Existing Data
    # -----------------------------
    Alert.query.delete()
    Report.query.delete()
    ProjectMetric.query.delete()
    ProjectLocation.query.delete()
    ProjectTeamMember.query.delete()
    ProjectDocument.query.delete()
    Risk.query.delete()
    Project.query.delete()
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
    # Lookup Foreign Keys
    # -----------------------------
    education = ProjectType.query.filter_by(name="Education").first()
    healthcare = ProjectType.query.filter_by(name="Healthcare").first()
    environment = ProjectType.query.filter_by(name="Environment").first()
    women_emp = ProjectType.query.filter_by(name="Women Empowerment").first()
    livelihood = ProjectType.query.filter_by(name="Livelihood").first()
    rural_dev = ProjectType.query.filter_by(name="Rural Development").first()

    students = BeneficiaryCategory.query.filter_by(name="Students").first()
    women = BeneficiaryCategory.query.filter_by(name="Women").first()
    children = BeneficiaryCategory.query.filter_by(name="Children").first()
    farmers = BeneficiaryCategory.query.filter_by(name="Farmers").first()

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

    db.session.add_all(projects)

    db.session.commit()

    print("Projects inserted.")

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

    ]

    db.session.add_all(risks)

    db.session.commit()

    print("Risks inserted.")

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

    print("Database seeded successfully!")