from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.finance_operation import FinanceCategory, FinanceOperationType

FINANCE_DESCRIPTION_MAX_LENGTH = 255

INCOME_CATEGORIES = {
    FinanceCategory.donations,
    FinanceCategory.sponsorship,
    FinanceCategory.grants,
    FinanceCategory.sales,
    FinanceCategory.other_income,
}

EXPENSE_CATEGORIES = {
    FinanceCategory.medications,
    FinanceCategory.feed,
    FinanceCategory.care,
    FinanceCategory.equipment,
    FinanceCategory.transport,
    FinanceCategory.repair,
    FinanceCategory.utilities,
    FinanceCategory.other_expense,
}


class FinanceOperationHorseRead(BaseModel):
    id: int
    name: str


class FinanceOperationCreate(BaseModel):
    operation_type: FinanceOperationType
    amount: Decimal = Field(gt=0, decimal_places=2, max_digits=12)
    category: FinanceCategory
    description: str = Field(min_length=1, max_length=FINANCE_DESCRIPTION_MAX_LENGTH)
    date: datetime
    horse_id: int | None = None

    @field_validator("description")
    @classmethod
    def validate_trimmed_description(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Поле не может быть пустым")
        return trimmed

    @model_validator(mode="after")
    def validate_category_matches_type(self):
        if self.operation_type == FinanceOperationType.income and self.category not in INCOME_CATEGORIES:
            raise ValueError("Категория не подходит для дохода")

        if self.operation_type == FinanceOperationType.expense and self.category not in EXPENSE_CATEGORIES:
            raise ValueError("Категория не подходит для расхода")

        return self


class FinanceOperationRead(BaseModel):
    id: int
    operation_type: FinanceOperationType
    amount: Decimal
    category: FinanceCategory
    description: str
    date: datetime
    horse_id: int | None
    created_at: datetime
    updated_at: datetime
    horse: FinanceOperationHorseRead | None = None

    model_config = {
        "from_attributes": True,
    }


class FinanceSummaryRead(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
