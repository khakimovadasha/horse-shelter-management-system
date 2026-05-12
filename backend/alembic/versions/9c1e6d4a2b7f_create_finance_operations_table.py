"""create finance operations table

Revision ID: 9c1e6d4a2b7f
Revises: f2b7d0d9c8a1
Create Date: 2026-05-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9c1e6d4a2b7f"
down_revision: Union[str, Sequence[str], None] = "f2b7d0d9c8a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "finance_operations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "operation_type",
            sa.Enum("income", "expense", name="finance_operation_type_enum"),
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "donations",
                "sponsorship",
                "grants",
                "sales",
                "other_income",
                "medications",
                "feed",
                "care",
                "equipment",
                "transport",
                "repair",
                "utilities",
                "other_expense",
                name="finance_category_enum",
            ),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("horse_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["horse_id"], ["horses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_finance_operations_id"),
        "finance_operations",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_finance_operations_id"), table_name="finance_operations")
    op.drop_table("finance_operations")
