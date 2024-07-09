"""Fix migration state

Revision ID: 213de7c66a41
Revises: 84b3b7ec198c
Create Date: 2024-07-09 19:13:25.712956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '213de7c66a41'
down_revision: Union[str, None] = '84b3b7ec198c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
