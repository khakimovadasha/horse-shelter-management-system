from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import datetime
from app.api.auth import get_current_user, require_admin_or_veterinarian
from app.db.session import get_db
from app.models.horse import Horse
from app.models.medical_record import MedicalRecord
from app.models.user import User
from app.schemas.medical_record import (
    MedicalRecordCreate,
    MedicalRecordHorseRead,
    MedicalRecordRead,
)

router = APIRouter(prefix="/horses", tags=["Medical Records"])


def serialize_medical_record(record: MedicalRecord, db: Session) -> MedicalRecordRead:
    horse_payload = None

    horse = db.execute(
        select(Horse).where(Horse.id == record.horse_id)
    ).scalar_one_or_none()
    if horse is not None:
        horse_payload = MedicalRecordHorseRead(
            id=horse.id,
            name=horse.name,
        )

    return MedicalRecordRead(
        id=record.id,
        horse_id=record.horse_id,
        record_date=record.record_date,
        record_type=record.record_type,
        title=record.title,
        description=record.description,
        created_at=record.created_at,
        updated_at=record.updated_at,
        horse=horse_payload,
    )


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

    return [serialize_medical_record(record, db) for record in records]


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
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return serialize_medical_record(new_record, db)
