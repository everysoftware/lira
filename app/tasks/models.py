from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models import Entity
from app.base.types import UUID
from app.tasks.schemas import TaskStatus, TestStatus

if TYPE_CHECKING:
    from app.lists.models import TodoList
    from app.users.models import User
    from app.workspaces.models import Workspace


class Task(Entity):
    __tablename__ = "tasks"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )
    workspace_id: Mapped[UUID] = mapped_column(
        ForeignKey("workspaces.id", ondelete="cascade")
    )
    todo_list_id: Mapped[UUID] = mapped_column(
        ForeignKey("todo_lists.id", ondelete="cascade")
    )
    name: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.to_do)
    test_status: Mapped[TestStatus] = mapped_column(
        default=TestStatus.no_status
    )
    report_url: Mapped[str | None]

    user: Mapped[User] = relationship(back_populates="tasks")
    workspace: Mapped[Workspace] = relationship(back_populates="tasks")
    todo_list: Mapped[TodoList] = relationship(back_populates="tasks")
