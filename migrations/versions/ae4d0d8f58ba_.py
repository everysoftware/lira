"""empty message

Revision ID: ae4d0d8f58ba
Revises: 
Create Date: 2023-11-17 17:56:01.778507

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ae4d0d8f58ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=True),
                    sa.Column('language_code', sa.String(), nullable=True),
                    sa.Column('username', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('id'),
                    sa.UniqueConstraint('user_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
