"""merge heads

Revision ID: ed4acce0bce4
Revises: 3b95f9fc5879, 5db835f7cbb0
Create Date: 2026-04-18 20:43:21.286291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed4acce0bce4'
down_revision: Union[str, Sequence[str], None] = ('3b95f9fc5879', '5db835f7cbb0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
