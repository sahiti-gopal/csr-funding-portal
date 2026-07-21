import os

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models import Role, User

load_dotenv()

DEMO_USERS = [
    {
        "first_name": os.getenv("SEED_ADMIN_FIRST_NAME", "CSR"),
        "last_name": os.getenv("SEED_ADMIN_LAST_NAME", "Admin"),
        "email": os.getenv("SEED_ADMIN_EMAIL", "admin@sevaimpact.org"),
        "password": os.getenv("SEED_ADMIN_PASSWORD", "Admin@123"),
        "role_name": "CSR Admin",
    },
]

app = create_app()

with app.app_context():
    for u in DEMO_USERS:
        if User.query.filter_by(email=u["email"]).first():
            print(f"skip (exists): {u['email']}")
            continue

        role = Role.query.filter_by(name=u["role_name"]).first()
        if not role:
            print(f"skip (missing role '{u['role_name']}'): {u['email']}")
            continue

        db.session.add(
            User(
                first_name=u["first_name"],
                last_name=u["last_name"],
                email=u["email"],
                password_hash=generate_password_hash(u["password"]),
                role_id=role.id,
            )
        )
        print(f"created: {u['email']} / {u['password']}")

    db.session.commit()
