"""add updated_at to users

Revision ID: e46218ee7358
Revises: 21df2b32e8fb
Create Date: 2026-08-23 13:27:47.200527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e46218ee7358'
down_revision: Union[str, Sequence[str], None] = '21df2b32e8fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True
        )
    )
### end Alembic commands ###


def downgrade() -> None:
    op.drop_column("users", "updated_at")
