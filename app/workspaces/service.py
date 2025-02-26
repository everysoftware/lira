from typing import Any

from app.base.pagination import Pagination, Page
from app.base.types import UUID
from app.base.use_case import UseCase
from app.db.dependencies import UOWDep
from app.users.models import User
from app.workspaces.models import Workspace
from app.workspaces.repositories import UserWorkspaceSpecification


class WorkspaceUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_many(
        self, user: User, pagination: Pagination
    ) -> Page[Workspace]:
        return await self.uow.workspaces.get_many(
            UserWorkspaceSpecification(user.id), pagination
        )

    async def create(self, **kwargs: Any) -> Workspace:
        workspace = Workspace(**kwargs)
        await self.uow.workspaces.add(workspace)
        await self.uow.commit()
        return workspace

    async def get_one(self, todo_list_id: UUID) -> Workspace:
        return await self.uow.workspaces.get_one(todo_list_id)
