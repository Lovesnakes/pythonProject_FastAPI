"""empty message

Revision ID: acc7b825eb69
Revises: e4c9eb0340d5
Create Date: 2024-01-23 20:42:39.159786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acc7b825eb69'
down_revision: Union[str, None] = 'e4c9eb0340d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
