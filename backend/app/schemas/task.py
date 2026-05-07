from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.task import TaskStatus

TASK_TITLE_MAX_LENGTH = 100
TASK_DESCRIPTION_MAX_LENGTH = 255


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=TASK_TITLE_MAX_LENGTH)
    description: str = Field(min_length=1, max_length=TASK_DESCRIPTION_MAX_LENGTH)
    horse_id: int | None = None
    due_date: datetime

    @field_validator("title", "description")
    @classmethod
    def validate_trimmed_text(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Поле не может быть пустым")
        return trimmed


class TaskHorseRead(BaseModel):
    id: int
    name: str


class TaskExecutorRead(BaseModel):
    id: int
    first_name: str
    last_name: str


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
    horse: TaskHorseRead | None = None
    executor: TaskExecutorRead | None = None

    model_config = {
        "from_attributes": True,
    }
