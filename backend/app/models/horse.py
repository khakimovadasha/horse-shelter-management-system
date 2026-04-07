from datetime import date, datetime
from enum import Enum

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HorseGender(str, Enum):
    male = "male"
    female = "female"


class HorseStatus(str, Enum):
    healthy = "healthy"
    sick = "sick"
    rehabilitation = "rehabilitation"
    deceased = "deceased"


class Horse(Base):
    __tablename__ = "horses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    gender: Mapped[HorseGender] = mapped_column(
        SqlEnum(HorseGender, name="horse_gender_enum"),
        nullable=False,
    )

    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    breed: Mapped[str | None] = mapped_column(String(50), nullable=True)
    color: Mapped[str | None] = mapped_column(String(50), nullable=True)

    arrival_date: Mapped[date] = mapped_column(Date, nullable=False)

    status: Mapped[HorseStatus] = mapped_column(
        SqlEnum(HorseStatus, name="horse_status_enum"),
        nullable=False,
        default=HorseStatus.healthy,
    )

    curator_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    history: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )