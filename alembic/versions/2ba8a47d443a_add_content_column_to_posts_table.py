"""add content column to posts table

Revision ID: 2ba8a47d443a
Revises: 8e3a0eb4d4bf
Create Date: 2024-10-22 20:09:04.183839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ba8a47d443a'
down_revision: Union[str, None] = '8e3a0eb4d4bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
