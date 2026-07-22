import os

from sqlalchemy import text

from app import create_app
from app.extensions import db
from app.models import Role

app = create_app()


def ensure_seeded():
    """First-run bootstrap: if the database is empty, seed it automatically
    before the app starts serving requests. Guarded by a MySQL advisory
    lock so multiple gunicorn workers starting at once don't double-seed.

    This must only run when the server actually starts (gunicorn's
    `when_ready` hook, or `app.run()` below for local dev) — never as a
    bare module-level side effect. `FLASK_APP=run.py` means `flask db
    upgrade` also imports this module to resolve the app object, and if
    seeding ran on import it would race the migration it depends on.
    """
    if os.getenv("AUTO_SEED", "true").lower() == "false":
        return

    with app.app_context():
        lock_conn = db.engine.connect()
        try:
            lock_conn.execute(text("SELECT GET_LOCK('csr_seed_lock', 30)"))

            # Drop any cached session so the next query sees a fresh
            # snapshot, in case another worker just committed the seed
            # while we waited.
            db.session.remove()

            if Role.query.first() is not None:
                print("Seed data already present — skipping auto-seed.")
                return

            print("No seed data found — seeding database...")

            import seed

            seed.run_seed()

            print("Auto-seed complete.")
        except Exception as exc:
            db.session.rollback()
            print(f"Auto-seed skipped due to error: {exc}")
        finally:
            lock_conn.execute(text("SELECT RELEASE_LOCK('csr_seed_lock')"))
            lock_conn.close()


if __name__ == "__main__":
    ensure_seeded()
    app.run(debug=True)
