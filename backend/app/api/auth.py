from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password, get_password_hash
from app.db.session import get_db
from app.models.horse import Horse
from app.models.role import Role
from app.models.task import Task
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    MeResponse,
    TokenResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.schemas.horse import HorseRead
from app.schemas.task import TaskExecutorRead, TaskHorseRead, TaskRead
from app.schemas.user import UserProfileSummaryRead

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить пользователя",
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


def require_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    role = db.execute(
        select(Role).where(Role.id == current_user.role_id)
    ).scalar_one_or_none()

    if role is None or role.code != "admin":
        raise HTTPException(status_code=403, detail="Нет доступа")

    return current_user

def require_admin_or_veterinarian(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    role = db.execute(
        select(Role).where(Role.id == current_user.role_id)
    ).scalar_one_or_none()

    if role is None or role.code not in ["admin", "veterinarian"]:
        raise HTTPException(status_code=403, detail="Нет доступа")

    return current_user


def build_curator_name(user: User | None) -> str | None:
    if user is None:
        return None
    return f"{user.first_name} {user.last_name}".strip()


def serialize_horse_for_me(horse: Horse, curator: User | None = None) -> HorseRead:
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


def serialize_task_for_me(task: Task, db: Session) -> TaskRead:
    horse_payload = None
    executor_payload = None

    if task.horse_id is not None:
        horse = db.execute(
            select(Horse).where(Horse.id == task.horse_id)
        ).scalar_one_or_none()
        if horse is not None:
            horse_payload = TaskHorseRead(
                id=horse.id,
                name=horse.name,
            )

    if task.executor_id is not None:
        executor = db.execute(
            select(User).where(User.id == task.executor_id)
        ).scalar_one_or_none()
        if executor is not None:
            executor_payload = TaskExecutorRead(
                id=executor.id,
                first_name=executor.first_name,
                last_name=executor.last_name,
            )

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        horse_id=task.horse_id,
        due_date=task.due_date,
        status=task.status,
        executor_id=task.executor_id,
        started_at=task.started_at,
        completed_at=task.completed_at,
        created_at=task.created_at,
        horse=horse_payload,
        executor=executor_payload,
    )


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_email = db.execute(
        select(User).where(User.email == data.email)
    ).scalar_one_or_none()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    if data.username:
        existing_username = db.execute(
            select(User).where(User.username == data.username)
        ).scalar_one_or_none()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username уже занят")

    user_role = db.execute(
        select(Role).where(Role.code == "user")
    ).scalar_one_or_none()
    if user_role is None:
        raise HTTPException(status_code=500, detail="Роль user не найдена")

    new_user = User(
        email=data.email,
        username=data.username,
        hashed_password=get_password_hash(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        role_id=user_role.id,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RegisterResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        phone=new_user.phone,
        role=user_role.code,
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=MeResponse)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.execute(select(Role).where(Role.id == current_user.role_id))
    role = result.scalar_one()

    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        phone=current_user.phone,
        role=role.code,
        is_active=current_user.is_active,
    )


@router.get("/me/profile-summary", response_model=UserProfileSummaryRead)
def me_profile_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    curated_horses_count = db.execute(
        select(func.count(Horse.id)).where(Horse.curator_id == current_user.id)
    ).scalar_one()

    my_tasks_count = db.execute(
        select(func.count(Task.id)).where(Task.executor_id == current_user.id)
    ).scalar_one()

    return UserProfileSummaryRead(
        curated_horses_count=curated_horses_count,
        my_tasks_count=my_tasks_count,
    )


@router.get("/me/horses", response_model=list[HorseRead])
def me_horses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    horses = db.execute(
        select(Horse)
        .where(Horse.curator_id == current_user.id)
        .order_by(Horse.id.desc())
    ).scalars().all()

    return [
        serialize_horse_for_me(horse, current_user)
        for horse in horses
    ]


@router.get("/me/tasks", response_model=list[TaskRead])
def me_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tasks = db.execute(
        select(Task)
        .where(Task.executor_id == current_user.id)
        .order_by(Task.due_date.desc(), Task.id.desc())
    ).scalars().all()

    return [serialize_task_for_me(task, db) for task in tasks]
