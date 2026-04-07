from datetime import date, datetime
from pydantic import BaseModel

from app.models.horse import HorseGender, HorseStatus


class HorseRead(BaseModel):
    id: int
    name: str
    gender: HorseGender
    age: int | None = None
    breed: str | None = None
    color: str | None = None
    arrival_date: date
    status: HorseStatus
    curator_id: int | None = None
    description: str | None = None
    history: str | None = None
    photo_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }