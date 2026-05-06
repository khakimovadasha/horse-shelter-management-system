"""create tasks table

Revision ID: c4e2f6b9a1d3
Revises: a15c1b5b8d6b
Create Date: 2026-05-06 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4e2f6b9a1d3"
down_revision: Union[str, Sequence[str], None] = "a15c1b5b8d6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("horse_id", sa.Integer(), nullable=True),
        sa.Column("due_date", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("waiting", "in_progress", "completed", name="task_status_enum"),
            nullable=False,
        ),
        sa.Column("executor_id", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["executor_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["horse_id"], ["horses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasks_id"), "tasks", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tasks_id"), table_name="tasks")
    op.drop_table("tasks")
