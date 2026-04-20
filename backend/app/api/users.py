from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


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