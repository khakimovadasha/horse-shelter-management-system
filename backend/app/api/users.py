from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserRead, UpdateUserRoleRequest, UpdateUserActiveRequest

router = APIRouter(prefix="/users", tags=["Users"])


# только для админа

@router.get("/", response_model=list[UserRead])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_role = db.execute(
        select(Role).where(Role.id == current_user.role_id)
    ).scalar_one_or_none()

    if current_role is None or current_role.code != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()

    result = []
    for user in users:
        role = db.execute(select(Role).where(Role.id == user.role_id)).scalar_one()
        result.append(
            UserRead(
                id=user.id,
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                phone=user.phone,
                is_active=user.is_active,
                role=role.code,
            )
        )

    return result


@router.patch("/{user_id}/role", response_model=UserRead)
def update_user_role(
    user_id: int,
    data: UpdateUserRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_role = db.execute(
        select(Role).where(Role.id == current_user.role_id)
    ).scalar_one_or_none()

    if current_role is None or current_role.code != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    new_role = db.execute(
        select(Role).where(Role.code == data.role)
    ).scalar_one_or_none()

    if new_role is None:
        raise HTTPException(status_code=400, detail="Роль не найдена")

    user.role_id = new_role.id
    db.commit()
    db.refresh(user)

    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        is_active=user.is_active,
        role=new_role.code,
    )


@router.patch("/{user_id}/active", response_model=UserRead)
def update_user_active(
    user_id: int,
    data: UpdateUserActiveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_role = db.execute(
        select(Role).where(Role.id == current_user.role_id)
    ).scalar_one_or_none()

    if current_role is None or current_role.code != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    user = db.execute(
        select(User).where(User.id == user_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.is_active = data.is_active
    db.commit()
    db.refresh(user)

    user_role = db.execute(
        select(Role).where(Role.id == user.role_id)
    ).scalar_one()

    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        is_active=user.is_active,
        role=user_role.code,
    )