"""upgrade variant head

Revision ID: cb77a8fca378
Revises: 6bbe562397fe
Create Date: 2024-07-30 12:14:00.613387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb77a8fca378'
down_revision: Union[str, None] = '6bbe562397fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_variants', sa.Column('media_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product_variants', 'media_galleries', ['media_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_variants', type_='foreignkey')
    op.drop_column('product_variants', 'media_id')
    # ### end Alembic commands ###
