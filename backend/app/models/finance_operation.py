from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FinanceOperationType(str, Enum):
    income = "income"
    expense = "expense"


class FinanceCategory(str, Enum):
    donations = "donations"
    sponsorship = "sponsorship"
    grants = "grants"
    sales = "sales"
    other_income = "other_income"
    medications = "medications"
    feed = "feed"
    care = "care"
    equipment = "equipment"
    transport = "transport"
    repair = "repair"
    utilities = "utilities"
    other_expense = "other_expense"


class FinanceOperation(Base):
    __tablename__ = "finance_operations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    operation_type: Mapped[FinanceOperationType] = mapped_column(
        SqlEnum(FinanceOperationType, name="finance_operation_type_enum"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    category: Mapped[FinanceCategory] = mapped_column(
        SqlEnum(FinanceCategory, name="finance_category_enum"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    horse_id: Mapped[int | None] = mapped_column(ForeignKey("horses.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
