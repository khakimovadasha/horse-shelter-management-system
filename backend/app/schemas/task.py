from datetime import datetime

from pydantic import BaseModel, Field

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    horse_id: int | None = None
    due_date: datetime


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    horse_id: int | None
    due_date: datetime
    status: TaskStatus
    executor_id: int | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
