"""create reports table

Revision ID: 40cda3f3cbaa
Revises: 62e2c48b74bb
Create Date: 2026-07-16 20:13:29.118476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40cda3f3cbaa'
down_revision = '62e2c48b74bb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("donor_id", sa.Integer(), sa.ForeignKey("donors.id"), nullable=False),
        sa.Column("financial_year", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("review_status", sa.String(length=30), nullable=False, server_default="Pending review"),
        sa.Column("delivery_status", sa.String(length=30), nullable=False, server_default="Awaiting"),
        sa.Column("generated_at", sa.DateTime(), nullable=True),
        sa.Column("content", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("donor_id", "financial_year", name="uq_report_donor_fy"),
    )


def downgrade():
    op.drop_table("reports")
