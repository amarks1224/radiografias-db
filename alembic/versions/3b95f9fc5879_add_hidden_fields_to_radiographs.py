"""add hidden fields to radiographs

Revision ID: 3b95f9fc5879
Revises: eb81ecdaf0df
Create Date: 2026-04-18 18:14:14.971845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3b95f9fc5879'
down_revision: Union[str, Sequence[str], None] = '5db835f7cbb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'radiographs',
        sa.Column('is_hidden', sa.Boolean(), nullable=False, server_default=sa.text('0'))
    )
    op.add_column(
        'radiographs',
        sa.Column('hidden_at', sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('radiographs', 'hidden_at')
    op.drop_column('radiographs', 'is_hidden')