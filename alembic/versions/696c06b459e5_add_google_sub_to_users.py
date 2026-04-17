"""add google_sub to users

Revision ID: 696c06b459e5
Revises: f0e0fd47b6fc
Create Date: 2026-04-16 20:41:22.777740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '696c06b459e5'
down_revision: Union[str, Sequence[str], None] = 'f0e0fd47b6fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("google_sub", sa.String(length=255), nullable=True))
        batch_op.create_unique_constraint("uq_users_google_sub", ["google_sub"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_constraint("uq_users_google_sub", type_="unique")
        batch_op.drop_column("google_sub")