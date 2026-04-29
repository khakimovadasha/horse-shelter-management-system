from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.medical_record import MedicalRecord, MedicalRecordType
from app.models.procedure import Procedure, ProcedureStatus


def complete_procedure_entity(
    procedure: Procedure,
    db: Session,
    completed_date: datetime | None = None,
) -> Procedure:
    if procedure.status == ProcedureStatus.completed:
        raise HTTPException(status_code=400, detail="Процедура уже выполнена")

    completed_at = completed_date or datetime.utcnow()

    procedure.status = ProcedureStatus.completed
    procedure.completed_date = completed_at

    if procedure.add_to_medical_record:
        medical_record = MedicalRecord(
            horse_id=procedure.horse_id,
            record_date=completed_at,
            record_type=MedicalRecordType.procedure,
            title=procedure.procedure_name,
            description=procedure.notes or procedure.procedure_name,
            next_procedure_date=None,
        )
        db.add(medical_record)

    return procedure
