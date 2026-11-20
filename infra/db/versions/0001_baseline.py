"""Create the empty Meterproof application schema."""

from __future__ import annotations

from alembic import op


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA meterproof")


def downgrade() -> None:
    op.execute("DROP SCHEMA meterproof")
