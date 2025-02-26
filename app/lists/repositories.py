from dataclasses import dataclass
from typing import Any

from app.base.specification import ISpecification
from app.base.types import UUID
from app.db.repository import SQLAlchemyRepository
from app.lists.models import TodoList


@dataclass
class UserTodoListSpecification(ISpecification):
    user_id: UUID

    def apply(self, stmt: Any) -> Any:
        return stmt.where(TodoList.user_id == self.user_id)


class TodoListRepository(SQLAlchemyRepository[TodoList]):
    model_type = TodoList
