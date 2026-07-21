"""add file_path to payment_documents

Revision ID: a1b2c3d4e5f6
Revises: 71965a7507c9
Create Date: 2026-07-21 10:10:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '71965a7507c9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('payment_documents', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_path', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('payment_documents', schema=None) as batch_op:
        batch_op.drop_column('file_path')
