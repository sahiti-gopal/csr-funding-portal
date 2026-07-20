"""add logo_url to donors

Revision ID: cea622944226
Revises: 40cda3f3cbaa
Create Date: 2026-07-18 21:42:35.710878

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cea622944226'
down_revision = '40cda3f3cbaa'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('donors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('logo_url', sa.String(length=300), nullable=True))


def downgrade():
    with op.batch_alter_table('donors', schema=None) as batch_op:
        batch_op.drop_column('logo_url')
