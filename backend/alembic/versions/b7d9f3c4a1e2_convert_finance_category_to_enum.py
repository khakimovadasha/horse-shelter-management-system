"""convert finance category to enum

Revision ID: b7d9f3c4a1e2
Revises: 9c1e6d4a2b7f
Create Date: 2026-05-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7d9f3c4a1e2"
down_revision: Union[str, Sequence[str], None] = "9c1e6d4a2b7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


finance_category_enum = sa.Enum(
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
)


def upgrade() -> None:
    bind = op.get_bind()
    finance_category_enum.create(bind, checkfirst=True)

    op.alter_column(
        "finance_operations",
        "category",
        existing_type=sa.String(length=100),
        type_=finance_category_enum,
        existing_nullable=False,
        postgresql_using="category::finance_category_enum",
    )


def downgrade() -> None:
    op.alter_column(
        "finance_operations",
        "category",
        existing_type=finance_category_enum,
        type_=sa.String(length=100),
        existing_nullable=False,
        postgresql_using="category::text",
    )

    bind = op.get_bind()
    finance_category_enum.drop(bind, checkfirst=True)
