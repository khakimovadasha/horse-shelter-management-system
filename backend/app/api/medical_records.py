from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime
from app.api.auth import get_current_user, require_admin_or_veterinarian
from app.db.session import get_db
from app.models.medical_record import MedicalRecord
from app.models.user import User
from app.schemas.medical_record import MedicalRecordRead, MedicalRecordCreate

router = APIRouter(prefix="/horses", tags=["Medical Records"])


@router.get("/{horse_id}/medical-records", response_model=list[MedicalRecordRead])
def get_medical_records_by_horse(
    horse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = db.execute(
        select(MedicalRecord)
        .where(MedicalRecord.horse_id == horse_id)
        .order_by(MedicalRecord.record_date.desc())
    ).scalars().all()

    return records


@router.post("/{horse_id}/medical-records", response_model=MedicalRecordRead)
def create_medical_record(
    horse_id: int,
    data: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_veterinarian),
):
    new_record = MedicalRecord(
        horse_id=horse_id,
        record_date=datetime.utcnow(),
        record_type=data.record_type,
        title=data.title,
        description=data.description,
        next_procedure_date=data.next_procedure_date,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record