"""Initial migration

Revision ID: d5b3a13e9e95
Revises: 
Create Date: 2024-09-21 02:37:04.622710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5b3a13e9e95'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'news_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('link', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('pub_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('news_items')
