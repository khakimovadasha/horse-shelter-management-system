from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.medical_record import MedicalRecord
from app.models.user import User
from app.schemas.medical_record import MedicalRecordRead

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