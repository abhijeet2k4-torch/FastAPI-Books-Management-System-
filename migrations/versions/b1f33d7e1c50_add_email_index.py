"""add email index

Revision ID: b1f33d7e1c50
Revises: 378d91b04a56
Create Date: 2026-06-21 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b1f33d7e1c50'
down_revision = '378d91b04a56'
branch_labels = None
depend_on = None


def upgrade() -> None:
    op.create_index('ix_users_email', 'users', ['email'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
