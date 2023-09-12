"""Add field_1 to users

Revision ID: 260b88fb5b7e
Revises: 78caea8126e5
Create Date: 2023-08-24 10:55:08.398866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '260b88fb5b7e'
down_revision: Union[str, None] = '78caea8126e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('field_1', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'field_1')
    # ### end Alembic commands ###