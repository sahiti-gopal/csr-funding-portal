import os

from sqlalchemy import text

from app import create_app
from app.extensions import db
from app.models import Role

app = create_app()


def _ensure_seeded():
    """First-run bootstrap: if the database is empty, seed it automatically
    before the app starts serving requests. Guarded by a MySQL advisory
    lock so multiple gunicorn workers starting at once don't double-seed.
    """
    if os.getenv("AUTO_SEED", "true").lower() == "false":
        return

    lock_conn = db.engine.connect()
    try:
        lock_conn.execute(text("SELECT GET_LOCK('csr_seed_lock', 30)"))

        # Drop any cached session so the next query sees a fresh snapshot,
        # in case another worker just committed the seed while we waited.
        db.session.remove()

        if Role.query.first() is not None:
            print("Seed data already present — skipping auto-seed.")
            return

        print("No seed data found — seeding database...")

        import seed
        import seed_users

        seed.run_seed()
        seed_users.run_seed_users()

        print("Auto-seed complete.")
    except Exception as exc:
        db.session.rollback()
        print(f"Auto-seed skipped due to error: {exc}")
    finally:
        lock_conn.execute(text("SELECT RELEASE_LOCK('csr_seed_lock')"))
        lock_conn.close()


with app.app_context():
    _ensure_seeded()

print("\n========== REGISTERED ROUTES ==========")

for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
    print(f"{rule.endpoint:35} {rule}")

print("=======================================\n")

if __name__ == "__main__":
    app.run(debug=True)