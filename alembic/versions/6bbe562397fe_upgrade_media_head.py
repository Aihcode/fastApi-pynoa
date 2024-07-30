"""upgrade media head

Revision ID: 6bbe562397fe
Revises: 468d1fdf48dd
Create Date: 2024-07-30 11:05:12.757637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bbe562397fe'
down_revision: Union[str, None] = '468d1fdf48dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media_galleries', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'media_galleries', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'media_galleries', type_='foreignkey')
    op.drop_column('media_galleries', 'user_id')
    # ### end Alembic commands ###