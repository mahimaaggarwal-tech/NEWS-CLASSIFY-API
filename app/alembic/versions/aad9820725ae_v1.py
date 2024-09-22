"""v1

Revision ID: aad9820725ae
Revises: 3fac289bdb57
Create Date: 2024-09-21 22:37:39.880509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aad9820725ae'
down_revision: Union[str, None] = '3fac289bdb57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    job_status_enum = sa.Enum('Processing', 'Completed', 'Failed', name='job_status_enum')

    op.create_table(
        'job_status',
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('status', job_status_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),  # Add created_at column
        sa.PrimaryKeyConstraint('job_id')
    )

def downgrade():
    op.drop_table('job_status')
    op.execute('DROP TYPE job_status_enum')

