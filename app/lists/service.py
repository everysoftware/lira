from typing import Any

from app.base.pagination import Pagination, Page
from app.base.types import UUID
from app.base.use_case import UseCase
from app.db.dependencies import UOWDep
from app.lists.models import TodoList
from app.lists.repositories import UserTodoListSpecification
from app.users.models import User


class TodoListUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_many(
        self, user: User, pagination: Pagination, **kwargs: Any
    ) -> Page[TodoList]:
        return await self.uow.todo_lists.get_many(
            UserTodoListSpecification(user.id), pagination, **kwargs
        )

    async def create(self, **kwargs: Any) -> TodoList:
        checklist = TodoList(**kwargs)
        await self.uow.todo_lists.add(checklist)
        await self.uow.commit()
        return checklist

    async def get_one(self, checklist_id: UUID) -> TodoList:
        return await self.uow.todo_lists.get_one(checklist_id)
