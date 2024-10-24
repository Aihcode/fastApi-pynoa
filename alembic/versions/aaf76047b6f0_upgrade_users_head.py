"""upgrade users head

Revision ID: aaf76047b6f0
Revises: 555e92464393
Create Date: 2024-08-23 11:50:58.620603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'aaf76047b6f0'
down_revision: Union[str, None] = '555e92464393'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('validation_code', sa.String(length=800), nullable=True))
    op.drop_column('users', 'validatetion_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('validatetion_code', mysql.VARCHAR(length=800), nullable=True))
    op.drop_column('users', 'validation_code')
    # ### end Alembic commands ###
