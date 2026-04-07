from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.horse import Horse
from app.schemas.horse import HorseRead

router = APIRouter(prefix="/horses", tags=["Horses"])


@router.get("/", response_model=list[HorseRead])
def get_horses(db: Session = Depends(get_db)):
    result = db.execute(select(Horse).order_by(Horse.id.desc()))
    horses = result.scalars().all()
    return horses