"""upgrade all models

Revision ID: 33f4193469dd
Revises: 59328e71dc2c
Create Date: 2024-07-14 19:37:46.010267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33f4193469dd'
down_revision: Union[str, None] = '59328e71dc2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
