from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, require_admin
from app.db.session import get_db
from app.models.horse import Horse
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead
from app.services.tasks import complete_task_entity, start_task_in_progress

router = APIRouter(tags=["Tasks"])


@router.get("/tasks", response_model=list[TaskRead])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = db.execute(
        select(Task).order_by(Task.due_date.desc(), Task.id.desc())
    ).scalars().all()

    return tasks


@router.get("/horses/{horse_id}/tasks", response_model=list[TaskRead])
def get_tasks_by_horse(
    horse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = db.execute(
        select(Task)
        .where(Task.horse_id == horse_id)
        .order_by(Task.due_date.desc(), Task.id.desc())
    ).scalars().all()

    return tasks


@router.post("/tasks", response_model=TaskRead)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if data.horse_id is not None:
        horse = db.execute(
            select(Horse).where(Horse.id == data.horse_id)
        ).scalar_one_or_none()
        if horse is None:
            raise HTTPException(status_code=404, detail="Лошадь не найдена")

    task = Task(
        title=data.title.strip(),
        description=data.description.strip(),
        horse_id=data.horse_id,
        due_date=data.due_date,
        status=TaskStatus.waiting,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.post("/tasks/{task_id}/start", response_model=TaskRead)
def start_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    start_task_in_progress(task=task, current_user=current_user)

    db.commit()
    db.refresh(task)

    return task


@router.post("/tasks/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    complete_task_entity(task=task, current_user=current_user)

    db.commit()
    db.refresh(task)

    return task
