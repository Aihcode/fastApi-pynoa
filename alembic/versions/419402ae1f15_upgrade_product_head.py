"""upgrade product head

Revision ID: 419402ae1f15
Revises: 69a4171a04c7
Create Date: 2024-08-15 12:44:14.739227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '419402ae1f15'
down_revision: Union[str, None] = '69a4171a04c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_variants', sa.Column('stripe_variant_id', sa.String(length=800), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product_variants', 'stripe_variant_id')
    # ### end Alembic commands ###
