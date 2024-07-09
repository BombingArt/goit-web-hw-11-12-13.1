"""Init

Revision ID: 541873c513ff
Revises: 5fa5a45ab3f5
Create Date: 2024-06-29 15:37:31.905993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "541873c513ff"
down_revision: Union[str, None] = "5fa5a45ab3f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


# Здесь необходимо указать индекс в соответствии с тем, что тебе нужно
def upgrade():
    # Добавь индекс, если он отсутствует
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade():
    # Удали индекс, если это нужно
    op.drop_index("ix_users_email", table_name="users")
