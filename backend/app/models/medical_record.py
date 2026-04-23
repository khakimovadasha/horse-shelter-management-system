from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, Text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MedicalRecordType(str, Enum):
    inspection = "inspection"
    diagnosis = "diagnosis"
    treatment = "treatment"
    analysis = "analysis"
    procedure = "procedure"
    note = "note"


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    horse_id: Mapped[int] = mapped_column(ForeignKey("horses.id"), nullable=False)

    record_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    record_type: Mapped[MedicalRecordType] = mapped_column(
        SqlEnum(MedicalRecordType, name="medical_record_type_enum"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    next_procedure_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )