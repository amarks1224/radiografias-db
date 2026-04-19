"""add google_sub to users

Revision ID: 5db835f7cbb0
Revises: f0e0fd47b6fc
Create Date: 2026-04-18 17:39:03.188685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5db835f7cbb0'
down_revision: Union[str, Sequence[str], None] = 'f0e0fd47b6fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('google_sub', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'google_sub')
