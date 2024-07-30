"""upgrade product head

Revision ID: 62be2fe1a370
Revises: 4b004a13f7b7
Create Date: 2024-07-30 12:29:19.012550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62be2fe1a370'
down_revision: Union[str, None] = '4b004a13f7b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_products_handle'), 'products', ['handle'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_products_handle'), table_name='products')
    # ### end Alembic commands ###