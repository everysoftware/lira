from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.models import Entity
from app.base.types import UUID

if TYPE_CHECKING:
    from app.lists.models import TodoList
    from app.tasks.models import Task
    from app.users.models import User


class Workspace(Entity):
    __tablename__ = "workspaces"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="cascade")
    )

    user: Mapped[User] = relationship(back_populates="workspaces")
    todo_lists: Mapped[list[TodoList]] = relationship(
        back_populates="workspace"
    )
    tasks: Mapped[list[Task]] = relationship(back_populates="workspace")
