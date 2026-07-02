"""create_scan_history_table

Revision ID: 48a2eb487a39
Revises: 
Create Date: 2026-07-01 16:57:23.750769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48a2eb487a39'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'scan_history',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('ip', sa.String(length=50), nullable=False),
        sa.Column('start_port', sa.Integer(), nullable=False),
        sa.Column('end_port', sa.Integer(), nullable=False),
        sa.Column('open_ports', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('scan_history')
