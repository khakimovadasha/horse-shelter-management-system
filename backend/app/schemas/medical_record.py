from datetime import datetime
from pydantic import BaseModel

from app.models.medical_record import MedicalRecordType


class MedicalRecordHorseRead(BaseModel):
    id: int
    name: str


class MedicalRecordRead(BaseModel):
    id: int
    horse_id: int
    record_date: datetime
    record_type: MedicalRecordType
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    horse: MedicalRecordHorseRead | None = None

    model_config = {
        "from_attributes": True
    }


class MedicalRecordCreate(BaseModel):
    record_type: MedicalRecordType
    title: str
    description: str
