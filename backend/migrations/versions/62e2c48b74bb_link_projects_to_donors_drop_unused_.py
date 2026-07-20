"""link projects to donors, drop unused payment tables

Revision ID: 62e2c48b74bb
Revises: e89a78643755
Create Date: 2026-07-16 19:02:57.002200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62e2c48b74bb'
down_revision = 'e89a78643755'
branch_labels = None
depends_on = None


def _existing_tables(bind):
    return set(sa.inspect(bind).get_table_names())


def upgrade():
    bind = op.get_bind()
    tables = _existing_tables(bind)

    # ------------------------------------------------------------
    # donor_payments / payment_documents were created out-of-band
    # (never tracked by an Alembic migration). Create them here if
    # a fresh DB doesn't have them yet, so `flask db upgrade` alone
    # is enough to reach a working schema.
    # ------------------------------------------------------------
    if "donor_payments" not in tables:
        op.create_table(
            "donor_payments",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("donor_id", sa.Integer(), sa.ForeignKey("donors.id"), nullable=False),
            sa.Column("installment_name", sa.String(length=100), nullable=False),
            sa.Column("amount", sa.Numeric(14, 2), nullable=False),
            sa.Column("due_date", sa.Date()),
            sa.Column("received_date", sa.Date()),
            sa.Column("payment_mode", sa.String(length=50)),
            sa.Column("transaction_id", sa.String(length=150)),
            sa.Column("status", sa.String(length=30), server_default="Pending"),
            sa.Column("remarks", sa.Text()),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        )

    if "payment_documents" not in tables:
        op.create_table(
            "payment_documents",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("payment_id", sa.Integer(), sa.ForeignKey("donor_payments.id"), nullable=False),
            sa.Column("document_name", sa.String(length=255), nullable=False),
            sa.Column("document_type", sa.String(length=50), nullable=False),
            sa.Column("file_url", sa.Text()),
            sa.Column("file_size", sa.String(length=30)),
            sa.Column("verification_status", sa.String(length=30), server_default="Pending"),
            sa.Column("uploaded_by", sa.String(length=150)),
            sa.Column("uploaded_at", sa.DateTime(), server_default=sa.func.now()),
        )

    # ------------------------------------------------------------
    # Link projects to donors with a real FK.
    # ------------------------------------------------------------
    op.add_column("projects", sa.Column("donor_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_projects_donor_id", "projects", "donors", ["donor_id"], ["id"]
    )

    # Best-effort backfill from the old free-text sponsor_name before
    # dropping it, so an existing dev DB doesn't silently lose the link.
    if "sponsor_name" in {c["name"] for c in sa.inspect(bind).get_columns("projects")}:
        op.execute(
            """
            UPDATE projects p
            JOIN donors d ON p.sponsor_name = d.name
            SET p.donor_id = d.id
            """
        )
        op.drop_column("projects", "sponsor_name")

    project_columns = {c["name"] for c in sa.inspect(bind).get_columns("projects")}
    if "sponsor_sector" in project_columns:
        op.drop_column("projects", "sponsor_sector")

    # ------------------------------------------------------------
    # Drop dead tables: never seeded, no longer referenced by any
    # model or route. project_donors is an orphaned, empty,
    # unreferenced many-to-many table with no corresponding model.
    # ------------------------------------------------------------
    for dead_table in ("fund_allocations", "payment_activity", "ai_payment_insights", "project_donors"):
        if dead_table in tables:
            op.drop_table(dead_table)

    # ------------------------------------------------------------
    # Conversation history for the NL->SQL chatbot.
    # ------------------------------------------------------------
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False, server_default="New conversation"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("messages")
    op.drop_table("conversations")

    op.create_table(
        "ai_payment_insights",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("donor_id", sa.Integer(), sa.ForeignKey("donors.id"), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_table(
        "payment_activity",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("donor_id", sa.Integer(), sa.ForeignKey("donors.id")),
        sa.Column("title", sa.String(length=255)),
        sa.Column("activity_type", sa.String(length=100)),
        sa.Column("activity_date", sa.DateTime()),
    )
    op.create_table(
        "fund_allocations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("donor_id", sa.Integer(), sa.ForeignKey("donors.id")),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id")),
        sa.Column("allocated_amount", sa.Numeric(14, 2)),
        sa.Column("utilized_amount", sa.Numeric(14, 2)),
        sa.Column("remaining_amount", sa.Numeric(14, 2)),
        sa.Column("allocation_date", sa.Date()),
    )

    op.add_column("projects", sa.Column("sponsor_sector", sa.String(length=150), nullable=True))
    op.add_column("projects", sa.Column("sponsor_name", sa.String(length=200), nullable=True))
    op.execute(
        """
        UPDATE projects p
        JOIN donors d ON p.donor_id = d.id
        SET p.sponsor_name = d.name
        """
    )
    op.drop_constraint("fk_projects_donor_id", "projects", type_="foreignkey")
    op.drop_column("projects", "donor_id")
