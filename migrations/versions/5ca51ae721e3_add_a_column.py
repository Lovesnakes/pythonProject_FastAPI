"""Add a column

Revision ID: 5ca51ae721e3
Revises: fba0ccd430a8
Create Date: 2024-01-21 15:25:34.688004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ca51ae721e3'
down_revision: Union[str, None] = 'fba0ccd430a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
