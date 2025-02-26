from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.base.models import Entity

if TYPE_CHECKING:
    from app.tasks.models import Task
    from app.lists.models import TodoList
    from app.workspaces.models import Workspace


class User(Entity):
    __tablename__ = "users"

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    telegram_id: Mapped[int] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    workspaces: Mapped[list[Workspace]] = relationship(back_populates="user")
    todo_lists: Mapped[list[TodoList]] = relationship(back_populates="user")
    tasks: Mapped[list[Task]] = relationship(back_populates="user")

    @hybrid_property
    def display_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return ""

    def grant_superuser(self) -> None:
        self.is_superuser = True
