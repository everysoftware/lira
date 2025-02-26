from aiogram.fsm.context import FSMContext

from app.base.use_case import UseCase
from app.db.dependencies import UOWDep
from app.lists.models import TodoList
from app.users.config import auth_settings
from app.users.models import User
from app.users.repositories import TelegramUserSpecification
from app.users.schemas import (
    UserCreate,
)
from app.workspaces.models import Workspace


class AuthUseCases(UseCase):
    def __init__(self, uow: UOWDep) -> None:
        self.uow = uow

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.uow.users.find(
            TelegramUserSpecification(telegram_id)
        )

    async def get_one_by_telegram_id(self, telegram_id: int) -> User:
        return await self.uow.users.find_one(
            TelegramUserSpecification(telegram_id)
        )

    async def register(self, state: FSMContext, data: UserCreate) -> User:
        if await self.get_by_telegram_id(data.telegram_id):
            raise ValueError()
        user = User.from_dto(data)
        if user.telegram_id == auth_settings.admin_telegram_id:
            user.grant_superuser()
        workspace = Workspace(
            name="Личное пространство",
            description="Личное пространство, которое создалось при регистрации",
            user=user,
        )
        todo_list = TodoList(
            name="Стандартный список",
            description="Стандартный список задач, который создался при регистрации",
            workspace=workspace,
            user=user,
        )
        user.workspaces.append(workspace)
        user.todo_lists.append(todo_list)
        await self.uow.users.add(user)
        await self.uow.commit()
        await state.update_data(
            workspace_id=str(workspace.id), todo_list_id=str(todo_list.id)
        )
        return user
