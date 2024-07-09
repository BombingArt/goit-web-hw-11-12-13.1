"""Fix migration state

Revision ID: 177d3d3b78ed
Revises: a32ccba8e689
Create Date: 2024-07-09 19:10:43.702927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '177d3d3b78ed'
down_revision: Union[str, None] = 'a32ccba8e689'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
