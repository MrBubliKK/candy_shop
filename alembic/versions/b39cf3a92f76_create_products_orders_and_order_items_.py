"""create products, orders, and order_items tables

Revision ID: b39cf3a92f76
Revises: 118e4b4f1958
Create Date: 2024-12-07 22:32:45.216835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b39cf3a92f76'
down_revision: Union[str, None] = '118e4b4f1958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
