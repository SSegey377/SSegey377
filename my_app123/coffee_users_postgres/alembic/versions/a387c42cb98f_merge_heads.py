"""Merge heads

Revision ID: a387c42cb98f
Revises: bacd24185044, fbce631bb25d
Create Date: 2025-05-26 14:29:42.062503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a387c42cb98f'
down_revision: Union[str, None] = ('bacd24185044', 'fbce631bb25d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
