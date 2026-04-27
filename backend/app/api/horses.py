from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import select
from sqlalchemy.orm import Session

import os
import shutil
from uuid import uuid4
from datetime import date

from app.db.session import get_db
from app.models.horse import Horse, HorseGender, HorseStatus
from app.schemas.horse import HorseRead
from app.api.auth import require_admin
from app.models.user import User

router = APIRouter(prefix="/horses", tags=["Horses"])


def build_curator_name(user: User | None) -> str | None:
    if user is None:
        return None
    return f"{user.first_name} {user.last_name}".strip()


def build_horse_response(horse: Horse, curator: User | None = None) -> HorseRead:
    return HorseRead(
        id=horse.id,
        name=horse.name,
        gender=horse.gender,
        age=horse.age,
        breed=horse.breed,
        color=horse.color,
        arrival_date=horse.arrival_date,
        status=horse.status,
        curator_id=horse.curator_id,
        curator_name=build_curator_name(curator),
        description=horse.description,
        history=horse.history,
        photo_url=horse.photo_url,
        is_active=horse.is_active,
        created_at=horse.created_at,
        updated_at=horse.updated_at,
    )


@router.get("/", response_model=list[HorseRead])
def get_horses(db: Session = Depends(get_db)):
    result = db.execute(select(Horse).order_by(Horse.id.desc()))
    horses = result.scalars().all()

    curator_ids = [horse.curator_id for horse in horses if horse.curator_id is not None]
    curators = {}

    if curator_ids:
        users = db.execute(
            select(User).where(User.id.in_(curator_ids))
        ).scalars().all()
        curators = {user.id: user for user in users}

    return [
        build_horse_response(horse, curators.get(horse.curator_id))
        for horse in horses
    ]


@router.get("/{horse_id}", response_model=HorseRead)
def get_horse(horse_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Horse).where(Horse.id == horse_id))
    horse = result.scalar_one_or_none()

    if horse is None:
        raise HTTPException(status_code=404, detail="Horse not found")

    curator = None
    if horse.curator_id is not None:
        curator = db.execute(
            select(User).where(User.id == horse.curator_id)
        ).scalar_one_or_none()

    return build_horse_response(horse, curator)


@router.post("/", response_model=HorseRead)
def create_horse(
    name: str = Form(..., min_length=1, max_length=50),
    gender: HorseGender = Form(...),
    age: int = Form(...),
    breed: str = Form(..., min_length=1, max_length=50),
    color: str = Form(..., min_length=1, max_length=50),
    status: HorseStatus = Form(...),
    curator_id: int | None = Form(None),
    description: str = Form(..., min_length=1, max_length=255),
    history: str = Form(..., min_length=1, max_length=1000),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if age < 0 or age > 50:
        raise HTTPException(status_code=400, detail="Возраст должен быть от 0 до 50")

    curator = None
    if curator_id is not None:
        curator = db.execute(
            select(User).where(User.id == curator_id)
        ).scalar_one_or_none()

        if curator is None or not curator.is_active:
            raise HTTPException(status_code=400, detail="Куратор не найден или неактивен")

    if not photo.content_type or not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    file_ext = os.path.splitext(photo.filename)[1].lower() if photo.filename else ""
    unique_filename = f"{uuid4().hex}{file_ext}"
    file_path = os.path.join("media", "horses", unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    new_horse = Horse(
        name=name,
        gender=gender,
        age=age,
        breed=breed,
        color=color,
        arrival_date=date.today(),
        status=status,
        curator_id=curator_id,
        description=description,
        history=history,
        photo_url=f"/media/horses/{unique_filename}",
        is_active=True,
    )

    db.add(new_horse)
    db.commit()
    db.refresh(new_horse)

    return build_horse_response(new_horse, curator)