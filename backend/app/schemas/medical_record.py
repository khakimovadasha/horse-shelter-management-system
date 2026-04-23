from datetime import datetime
from pydantic import BaseModel


class MedicalRecordRead(BaseModel):
    id: int
    horse_id: int
    record_date: datetime
    record_type: str
    title: str
    description: str
    next_procedure_date: datetime | None
    created_at: datetime
    updated_at: datetime


class MedicalRecordCreate(BaseModel):
    record_date: datetime
    record_type: str
    title: str
    description: str
    next_procedure_date: datetime | None = None