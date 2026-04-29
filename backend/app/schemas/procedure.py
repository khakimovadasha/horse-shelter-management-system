from datetime import datetime

from pydantic import BaseModel, Field

from app.models.procedure import ProcedureStatus


class ProcedureCreate(BaseModel):
    procedure_name: str = Field(min_length=1, max_length=100)
    notes: str | None = None
    planned_date: datetime
    add_to_medical_record: bool = False


class ProcedureRead(BaseModel):
    id: int
    horse_id: int
    procedure_name: str
    notes: str | None
    planned_date: datetime
    completed_date: datetime | None
    status: ProcedureStatus
    add_to_medical_record: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProcedureComplete(BaseModel):
    completed_date: datetime | None = None
