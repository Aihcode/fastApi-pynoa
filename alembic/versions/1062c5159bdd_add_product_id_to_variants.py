"""add product id to variants

Revision ID: 1062c5159bdd
Revises: f824cfc93c3b
Create Date: 2024-07-25 11:29:30.797896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1062c5159bdd'
down_revision: Union[str, None] = 'f824cfc93c3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_variants', 'price',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product_variants', 'price',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
