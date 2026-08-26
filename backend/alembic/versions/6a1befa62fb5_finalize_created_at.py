"""finalize created_at

Revision ID: 6a1befa62fb5
Revises: f478a18d5372
Create Date: 2026-08-23 13:00:28.083644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a1befa62fb5'
down_revision: Union[str, Sequence[str], None] = 'f478a18d5372'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE users SET created_at=CURRENT_TIMESTAMP "
        "WHERE created_at IS NULL"
    )
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        server_default=None
    )  
