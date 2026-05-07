"""drop next_procedure_date from medical_records

Revision ID: f2b7d0d9c8a1
Revises: c4e2f6b9a1d3
Create Date: 2026-05-07
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f2b7d0d9c8a1"
down_revision = "c4e2f6b9a1d3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("medical_records", "next_procedure_date")


def downgrade() -> None:
    op.add_column(
        "medical_records",
        sa.Column("next_procedure_date", sa.DateTime(), nullable=True),
    )
