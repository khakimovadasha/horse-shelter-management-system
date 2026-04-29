from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, require_admin_or_veterinarian
from app.db.session import get_db
from app.models.horse import Horse
from app.models.procedure import Procedure, ProcedureStatus
from app.models.user import User
from app.schemas.procedure import ProcedureCreate, ProcedureRead, ProcedureComplete
from app.services.procedures import complete_procedure_entity

router = APIRouter(tags=["Procedures"])


@router.get("/procedures", response_model=list[ProcedureRead])
def get_procedures(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    procedures = db.execute(
        select(Procedure)
        .order_by(Procedure.planned_date.asc(), Procedure.id.asc())
    ).scalars().all()

    return procedures


@router.get("/horses/{horse_id}/procedures", response_model=list[ProcedureRead])
def get_procedures_by_horse(
    horse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    procedures = db.execute(
        select(Procedure)
        .where(Procedure.horse_id == horse_id)
        .order_by(Procedure.planned_date.asc(), Procedure.id.asc())
    ).scalars().all()

    return procedures


@router.post("/horses/{horse_id}/procedures", response_model=ProcedureRead)
def create_procedure(
    horse_id: int,
    data: ProcedureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_veterinarian),
):
    horse = db.execute(select(Horse).where(Horse.id == horse_id)).scalar_one_or_none()
    if horse is None:
        raise HTTPException(status_code=404, detail="Лошадь не найдена")

    procedure = Procedure(
        horse_id=horse_id,
        procedure_name=data.procedure_name.strip(),
        notes=data.notes.strip() if data.notes else None,
        planned_date=data.planned_date,
        status=ProcedureStatus.planned,
        add_to_medical_record=data.add_to_medical_record,
    )

    db.add(procedure)
    db.commit()
    db.refresh(procedure)

    return procedure


@router.post("/horses/{horse_id}/procedures/{procedure_id}/complete", response_model=ProcedureRead)
def complete_procedure(
    horse_id: int,
    procedure_id: int,
    data: ProcedureComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_veterinarian),
):
    procedure = db.execute(
        select(Procedure).where(
            Procedure.id == procedure_id,
            Procedure.horse_id == horse_id,
        )
    ).scalar_one_or_none()

    if procedure is None:
        raise HTTPException(status_code=404, detail="Процедура не найдена")

    complete_procedure_entity(
        procedure=procedure,
        db=db,
        completed_date=data.completed_date,
    )

    db.commit()
    db.refresh(procedure)

    return procedure
