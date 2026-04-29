from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProcedureStatus(str, Enum):
    planned = "planned"
    completed = "completed"


class Procedure(Base):
    __tablename__ = "procedures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    horse_id: Mapped[int] = mapped_column(ForeignKey("horses.id"), nullable=False)

    procedure_name: Mapped[str] = mapped_column(String(100), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    planned_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    status: Mapped[ProcedureStatus] = mapped_column(
        SqlEnum(ProcedureStatus, name="procedure_status_enum"),
        nullable=False,
        default=ProcedureStatus.planned,
    )

    add_to_medical_record: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
