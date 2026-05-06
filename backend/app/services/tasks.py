from datetime import datetime

from fastapi import HTTPException

from app.models.task import Task, TaskStatus
from app.models.user import User


def start_task_in_progress(task: Task, current_user: User) -> Task:
    if task.status == TaskStatus.in_progress:
        raise HTTPException(status_code=400, detail="Задача уже взята в работу")

    if task.status == TaskStatus.completed:
        raise HTTPException(status_code=400, detail="Задача уже выполнена")

    task.status = TaskStatus.in_progress
    task.executor_id = current_user.id
    task.started_at = datetime.utcnow()

    return task


def complete_task_entity(task: Task, current_user: User) -> Task:
    if task.status == TaskStatus.waiting:
        raise HTTPException(
            status_code=400,
            detail="Нельзя завершить задачу, не взяв ее в работу",
        )

    if task.status == TaskStatus.completed:
        raise HTTPException(status_code=400, detail="Задача уже выполнена")

    if task.executor_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Завершить задачу может только ее исполнитель",
        )

    task.status = TaskStatus.completed
    task.completed_at = datetime.utcnow()

    return task
