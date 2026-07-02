"""create_users_table

Revision ID: 9cb14632d445
Revises: 48a2eb487a39
Create Date: 2026-07-01 21:51:19.538807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cb14632d445'
down_revision: Union[str, None] = '48a2eb487a39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), sa.Identity(start=1, increment=1), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email') # Эмейлы не должны повторяться
    )

def downgrade() -> None:
    op.drop_table('users')
