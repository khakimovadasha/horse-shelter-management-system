from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

import os
import shutil
from uuid import uuid4
from datetime import date

from app.db.session import get_db
from app.models.horse import Horse, HorseGender, HorseStatus
from app.schemas.horse import HorseRead
from app.api.auth import require_admin, require_admin_or_veterinarian
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


@router.patch("/{horse_id}", response_model=HorseRead)
async def update_horse(
    request: Request,
    horse_id: int,
    name: str | None = Form(None),
    gender: HorseGender | None = Form(None),
    age: int | None = Form(None),
    breed: str | None = Form(None),
    color: str | None = Form(None),
    arrival_date: date | None = Form(None),
    status: HorseStatus | None = Form(None),
    curator_id: str | None = Form(None),
    description: str | None = Form(None),
    history: str | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_veterinarian),
):
    result = db.execute(select(Horse).where(Horse.id == horse_id))
    horse = result.scalar_one_or_none()

    if horse is None:
        raise HTTPException(status_code=404, detail="Horse not found")

    form = await request.form()
    photo = form.get("photo")

    if name is not None:
        name = name.strip()
        if not name or len(name) > 50:
            raise HTTPException(status_code=400, detail="Имя должно быть от 1 до 50 символов")
        horse.name = name

    if gender is not None:
        horse.gender = gender

    if age is not None:
        if age < 0 or age > 50:
            raise HTTPException(status_code=400, detail="Возраст должен быть от 0 до 50")
        horse.age = age

    if breed is not None:
        breed = breed.strip()
        if not breed or len(breed) > 50:
            raise HTTPException(status_code=400, detail="Порода должна быть от 1 до 50 символов")
        horse.breed = breed

    if color is not None:
        color = color.strip()
        if not color or len(color) > 50:
            raise HTTPException(status_code=400, detail="Масть должна быть от 1 до 50 символов")
        horse.color = color

    if arrival_date is not None:
        horse.arrival_date = arrival_date

    if status is not None:
        horse.status = status

    if curator_id is not None:
        if curator_id == "":
            horse.curator_id = None
        else:
            try:
                curator_id_int = int(curator_id)
            except ValueError:
                raise HTTPException(status_code=400, detail="Некорректный curator_id")

            curator = db.execute(
                select(User).where(User.id == curator_id_int)
            ).scalar_one_or_none()

            if curator is None or not curator.is_active:
                raise HTTPException(status_code=400, detail="Куратор не найден или неактивен")

            horse.curator_id = curator_id_int

    if description is not None:
        description = description.strip()
        if not description or len(description) > 255:
            raise HTTPException(status_code=400, detail="Описание должно быть от 1 до 255 символов")
        horse.description = description

    if history is not None:
        history = history.strip()
        if not history or len(history) > 1000:
            raise HTTPException(status_code=400, detail="История должна быть от 1 до 1000 символов")
        horse.history = history

    if photo and isinstance(photo, UploadFile) and photo.filename:
        if not photo.content_type or not photo.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Файл должен быть изображением")

        file_ext = os.path.splitext(photo.filename)[1].lower() if photo.filename else ""
        unique_filename = f"{uuid4().hex}{file_ext}"
        file_path = os.path.join("media", "horses", unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        horse.photo_url = f"/media/horses/{unique_filename}"

    db.commit()
    db.refresh(horse)

    curator = None
    if horse.curator_id is not None:
        curator = db.execute(
            select(User).where(User.id == horse.curator_id)
        ).scalar_one_or_none()

    return build_horse_response(horse, curator)