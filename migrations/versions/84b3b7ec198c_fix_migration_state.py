"""Fix migration state

Revision ID: 84b3b7ec198c
Revises: 177d3d3b78ed
Create Date: 2024-07-09 19:12:16.613484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84b3b7ec198c'
down_revision: Union[str, None] = '177d3d3b78ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
