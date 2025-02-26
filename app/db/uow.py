from __future__ import annotations
from __future__ import annotations

import abc
from abc import ABC
from typing import Self, Any
from typing import cast

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.lists.repositories import TodoListRepository
from app.tasks.repositories import TaskRepository
from app.users.repositories import UserRepository
from app.workspaces.repositories import WorkspaceRepository


class IUnitOfWork(ABC):
    users: UserRepository
    tasks: TaskRepository
    todo_lists: TodoListRepository
    workspaces: WorkspaceRepository

    @abc.abstractmethod
    async def begin(self) -> None: ...

    @property
    @abc.abstractmethod
    def is_active(self) -> bool: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...

    @abc.abstractmethod
    async def close(self) -> None: ...

    async def __aenter__(self) -> Self:
        await self.begin()
        return self

    async def __aexit__(
        self, exc_type: Any, exc_value: Any, traceback: Any
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        await self.close()


class SQLAlchemyUOW(IUnitOfWork):
    _session_factory: async_sessionmaker[AsyncSession]
    _session: AsyncSession

    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        self._session_factory = session_factory

    async def begin(self) -> None:
        self._session = self._session_factory()
        self.users = UserRepository(self._session)
        self.tasks = TaskRepository(self._session)
        self.todo_lists = TodoListRepository(self._session)
        self.workspaces = WorkspaceRepository(self._session)

    @property
    def is_active(self) -> bool:
        if not self._session:
            return False
        return cast(bool, self._session.is_active)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close(self) -> None:
        await self._session.close()
