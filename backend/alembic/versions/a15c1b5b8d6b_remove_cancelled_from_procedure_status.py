"""remove cancelled from procedure status

Revision ID: a15c1b5b8d6b
Revises: 6da078f5770f
Create Date: 2026-04-29 23:20:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a15c1b5b8d6b"
down_revision: Union[str, Sequence[str], None] = "6da078f5770f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE procedures SET status = 'planned' WHERE status = 'cancelled'")
    op.execute("ALTER TABLE procedures ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TYPE procedure_status_enum RENAME TO procedure_status_enum_old")
    op.execute("CREATE TYPE procedure_status_enum AS ENUM ('planned', 'completed')")
    op.execute(
        """
        ALTER TABLE procedures
        ALTER COLUMN status TYPE procedure_status_enum
        USING status::text::procedure_status_enum
        """
    )
    op.execute("ALTER TABLE procedures ALTER COLUMN status SET DEFAULT 'planned'")
    op.execute("DROP TYPE procedure_status_enum_old")


def downgrade() -> None:
    op.execute("ALTER TABLE procedures ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TYPE procedure_status_enum RENAME TO procedure_status_enum_old")
    op.execute("CREATE TYPE procedure_status_enum AS ENUM ('planned', 'completed', 'cancelled')")
    op.execute(
        """
        ALTER TABLE procedures
        ALTER COLUMN status TYPE procedure_status_enum
        USING status::text::procedure_status_enum
        """
    )
    op.execute("ALTER TABLE procedures ALTER COLUMN status SET DEFAULT 'planned'")
    op.execute("DROP TYPE procedure_status_enum_old")
