from datetime import date

from app import create_app
from app.extensions import db
from app.models.project import Project
from app.models.alert import Alert

app = create_app()

with app.app_context():

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

    db.session.add_all(alerts)
    db.session.commit()

    print(f"Inserted {len(alerts)} alerts.")
