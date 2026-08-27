from sqlalchemy import text

from app.extensions import db

# Hand-written table/column list (not auto-introspected): keeps the prompt
# small and makes sure `users`/`roles` (auth tables) never enter the model's
# vocabulary. Actual *values* for low-cardinality columns are appended at
# request time by build_schema_description() below, straight from the DB,
# so the model never has to guess a format (e.g. "2026" vs "2026-27").
SCHEMA_TABLES = """\
projects(id, project_name, project_type_id, beneficiary_category_id, donor_id,
         budget, location, region, financial_year, status, start_date, end_date,
         raised_amount, utilized_amount, beneficiaries_reached)
donors(id, name, focus_area, likelihood, last_contact, status)
project_types(id, name, description, icon, color, is_active)
beneficiary_categories(id, name, description, icon, color, is_active)
alerts(id, title, description, category, priority, status, due_date, is_read, is_resolved, project_id)
risks(id, title, description, level, due_date, action)

-- projects.donor_id -> donors.id
-- projects.project_type_id -> project_types.id
-- projects.beneficiary_category_id -> beneficiary_categories.id
-- alerts.project_id -> projects.id
-- To filter/group projects by type or beneficiary category name, JOIN to
--   project_types / beneficiary_categories rather than guessing an id.
"""

# Columns worth showing the model real distinct values for, so it never has
# to guess a string format. Keep this small — only low-cardinality columns.
VALUE_SAMPLE_COLUMNS = [
    ("projects", "financial_year"),
    ("projects", "region"),
    ("projects", "status"),
    ("donors", "status"),
    ("donors", "focus_area"),
    ("risks", "level"),
    ("alerts", "category"),
    ("alerts", "priority"),
    ("alerts", "status"),
]

ALLOWED_TABLES = {
    "projects",
    "donors",
    "project_types",
    "beneficiary_categories",
    "alerts",
    "risks",
}

_schema_description_cache = None


def build_schema_description() -> str:
    """Schema text + real distinct values for key columns, cached for the
    life of the process (this is seed/demo data — it doesn't change shape
    mid-run, and re-querying it on every message would add latency)."""
    global _schema_description_cache
    if _schema_description_cache is not None:
        return _schema_description_cache

    lines = []
    for table, column in VALUE_SAMPLE_COLUMNS:
        rows = db.session.execute(
            text(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL LIMIT 20")
        ).fetchall()
        values = sorted({str(r[0]) for r in rows})
        if values:
            lines.append(f"- {table}.{column} values: {', '.join(values)}")

    notes = (
        "Column value notes (these are the ACTUAL values in the database — "
        "use them verbatim, never invent a different format):\n"
        + "\n".join(lines)
        + "\n- projects.financial_year is a fiscal-year range string like "
        "'2026-27'. If the user names a single year (e.g. \"FY 2026\" or "
        "\"2026\"), match with `financial_year LIKE '2026%'`, not an exact "
        "equality check against a bare year.\n"
    )

    _schema_description_cache = SCHEMA_TABLES + "\n" + notes
    return _schema_description_cache
