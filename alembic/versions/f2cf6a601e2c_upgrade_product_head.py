"""upgrade product head

Revision ID: f2cf6a601e2c
Revises: 419402ae1f15
Create Date: 2024-08-22 09:28:56.301373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f2cf6a601e2c'
down_revision: Union[str, None] = '419402ae1f15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('on_stripe', sa.Boolean(), nullable=True))
    op.drop_column('products', 'stripe_product_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('stripe_product_id', mysql.VARCHAR(length=800), nullable=True))
    op.drop_column('products', 'on_stripe')
    # ### end Alembic commands ###