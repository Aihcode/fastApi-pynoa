"""upgrade mail notifications head

Revision ID: 555e92464393
Revises: 143e3d631dc9
Create Date: 2024-08-23 11:37:50.295731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '555e92464393'
down_revision: Union[str, None] = '143e3d631dc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mail_notifications', sa.Column('from_param', sa.String(length=800), nullable=True))
    op.add_column('mail_notifications', sa.Column('to_list', sa.String(length=800), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mail_notifications', 'to_list')
    op.drop_column('mail_notifications', 'from_param')
    # ### end Alembic commands ###
