import re
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import ProjectType, BeneficiaryCategory
from app.models.project import Project

ROW_RE = re.compile(
    r"\('([^']*)',(\d+),(\d+),([\d.]+),'([^']*)','([^']*)','([^']*)','([^']*)',"
    r"'([^']*)','([^']*)','([^']*)','([^']*)',([\d.]+),([\d.]+),(\d+)"
)

app = create_app()

with app.app_context():
    project_types = ProjectType.query.order_by(ProjectType.id).all()
    categories = BeneficiaryCategory.query.order_by(BeneficiaryCategory.id).all()

    if not project_types or not categories:
        raise SystemExit("Run seed.py first — no project types/categories found.")

    with open("../portfolio_demo_data.sql", encoding="utf-8") as f:
        content = f.read()

    rows = ROW_RE.findall(content)

    if not rows:
        raise SystemExit("No rows parsed from portfolio_demo_data.sql")

    projects = []

    for i, row in enumerate(rows):
        (
            name,
            _old_type_id,
            _old_category_id,
            budget,
            location,
            region,
            fy,
            status,
            start_date,
            end_date,
            sponsor_name,
            sponsor_sector,
            raised,
            utilized,
            beneficiaries,
        ) = row

        projects.append(
            Project(
                project_name=name,
                project_type_id=project_types[i % len(project_types)].id,
                beneficiary_category_id=categories[i % len(categories)].id,
                budget=float(budget),
                location=location,
                region=region,
                financial_year=fy,
                status=status,
                start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
                sponsor_name=sponsor_name,
                sponsor_sector=sponsor_sector,
                raised_amount=float(raised),
                utilized_amount=float(utilized),
                beneficiaries_reached=int(beneficiaries),
            )
        )

    db.session.add_all(projects)
    db.session.commit()

    print(f"Imported {len(projects)} projects from portfolio_demo_data.sql")
