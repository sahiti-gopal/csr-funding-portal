"""create donor_documents table

Revision ID: 71965a7507c9
Revises: cea622944226
Create Date: 2026-07-21 09:59:40.723104

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '71965a7507c9'
down_revision = 'cea622944226'
branch_labels = None
depends_on = None


def upgrade():
    # NOTE: autogenerate also picked up pre-existing drift between the ORM
    # models and the live schema on several unrelated tables (donor_payments,
    # payment_documents, project_team_members, risks). That drift predates
    # this change and isn't part of it, so those operations were dropped from
    # this migration — only the new donor_documents table is created here.
    op.create_table('donor_documents',
    sa.Column('donor_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('severity', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('owner', sa.String(length=150), nullable=True),
    sa.Column('file_path', sa.Text(), nullable=True),
    sa.Column('file_size', sa.String(length=30), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['donor_id'], ['donors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('donor_documents')
