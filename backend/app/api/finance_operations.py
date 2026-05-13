from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import require_admin
from app.db.session import get_db
from app.models.finance_operation import FinanceOperation, FinanceOperationType
from app.models.horse import Horse
from app.models.user import User
from app.schemas.finance_operation import (
    FinanceOperationCreate,
    FinanceOperationHorseRead,
    FinanceOperationRead,
    FinanceOperationUpdate,
    FinanceSummaryRead,
    validate_finance_category_matches_type,
)

router = APIRouter(tags=["Finance"])


def serialize_finance_operation(operation: FinanceOperation, db: Session) -> FinanceOperationRead:
    horse_payload = None

    if operation.horse_id is not None:
        horse = db.execute(
            select(Horse).where(Horse.id == operation.horse_id)
        ).scalar_one_or_none()
        if horse is not None:
            horse_payload = FinanceOperationHorseRead(
                id=horse.id,
                name=horse.name,
            )

    return FinanceOperationRead(
        id=operation.id,
        operation_type=operation.operation_type,
        amount=operation.amount,
        category=operation.category,
        description=operation.description,
        date=operation.date,
        horse_id=operation.horse_id,
        created_at=operation.created_at,
        updated_at=operation.updated_at,
        horse=horse_payload,
    )


def ensure_horse_exists(horse_id: int | None, db: Session) -> None:
    if horse_id is None:
        return

    horse = db.execute(
        select(Horse).where(Horse.id == horse_id)
    ).scalar_one_or_none()
    if horse is None:
        raise HTTPException(status_code=404, detail="Лошадь не найдена")


@router.get("/finance-operations", response_model=list[FinanceOperationRead])
def get_finance_operations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operations = db.execute(
        select(FinanceOperation)
        .order_by(FinanceOperation.date.desc(), FinanceOperation.id.desc())
    ).scalars().all()

    return [serialize_finance_operation(operation, db) for operation in operations]


@router.get("/finance-operations/summary", response_model=FinanceSummaryRead)
def get_finance_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operations = db.execute(select(FinanceOperation)).scalars().all()

    total_income = sum(
        (operation.amount for operation in operations if operation.operation_type == FinanceOperationType.income),
        start=Decimal("0.00"),
    )
    total_expense = sum(
        (operation.amount for operation in operations if operation.operation_type == FinanceOperationType.expense),
        start=Decimal("0.00"),
    )

    return FinanceSummaryRead(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
    )


@router.post("/finance-operations", response_model=FinanceOperationRead)
def create_finance_operation(
    data: FinanceOperationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    ensure_horse_exists(data.horse_id, db)

    operation = FinanceOperation(
        operation_type=data.operation_type,
        amount=data.amount,
        category=data.category,
        description=data.description,
        date=data.date,
        horse_id=data.horse_id,
    )

    db.add(operation)
    db.commit()
    db.refresh(operation)

    return serialize_finance_operation(operation, db)


@router.patch("/finance-operations/{operation_id}", response_model=FinanceOperationRead)
def update_finance_operation(
    operation_id: int,
    data: FinanceOperationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operation = db.execute(
        select(FinanceOperation).where(FinanceOperation.id == operation_id)
    ).scalar_one_or_none()
    if operation is None:
        raise HTTPException(status_code=404, detail="Финансовая операция не найдена")

    payload = data.model_dump(exclude_unset=True)

    next_operation_type = payload.get("operation_type", operation.operation_type)
    next_category = payload.get("category", operation.category)

    try:
        validate_finance_category_matches_type(next_operation_type, next_category)
    except ValueError as err:
        raise HTTPException(status_code=422, detail=str(err)) from err

    if "horse_id" in payload:
        ensure_horse_exists(payload["horse_id"], db)

    for field_name, value in payload.items():
        setattr(operation, field_name, value)

    db.commit()
    db.refresh(operation)

    return serialize_finance_operation(operation, db)


@router.delete("/finance-operations/{operation_id}", status_code=204)
def delete_finance_operation(
    operation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    operation = db.execute(
        select(FinanceOperation).where(FinanceOperation.id == operation_id)
    ).scalar_one_or_none()
    if operation is None:
        raise HTTPException(status_code=404, detail="Финансовая операция не найдена")

    db.delete(operation)
    db.commit()

    return Response(status_code=204)
