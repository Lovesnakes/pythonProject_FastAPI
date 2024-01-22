"""empty message

Revision ID: e4c9eb0340d5
Revises: 5ca51ae721e3
Create Date: 2024-01-21 23:13:16.268570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4c9eb0340d5'
down_revision: Union[str, None] = '5ca51ae721e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
