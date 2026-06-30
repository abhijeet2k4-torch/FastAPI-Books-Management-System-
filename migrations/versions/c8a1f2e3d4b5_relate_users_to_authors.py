"""relate users to authors

Revision ID: c8a1f2e3d4b5
Revises: 4e6cb695a74a
Create Date: 2026-06-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c8a1f2e3d4b5'
down_revision: Union[str, Sequence[str], None] = '4e6cb695a74a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('authors', sa.Column('user_uid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'authors', 'users', ['user_uid'], ['uid'])


def downgrade() -> None:
    op.drop_constraint(None, 'authors', type_='foreignkey')
    op.drop_column('authors', 'user_uid')
