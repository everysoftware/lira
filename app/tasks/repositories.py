import datetime
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select, func

from app.base.specification import ISpecification
from app.base.types import UUID
from app.db.repository import SQLAlchemyRepository
from app.tasks.models import Task
from app.tasks.schemas import TaskStatus, TestStatus


@dataclass
class TodoListTaskSpecification(ISpecification):
    checklist_id: UUID

    def apply(self, stmt: Any) -> Any:
        return stmt.where(Task.todo_list_id == self.checklist_id)


class TaskRepository(SQLAlchemyRepository[Task]):
    model_type = Task

    async def get_task_stats(
        self,
        user_id: UUID,
        from_dt: datetime.datetime,
        to_dt: datetime.datetime,
    ) -> dict[datetime.datetime, int]:
        # Запрос на получение количества выполненных задач по дням за последний год
        stmt = (
            select(
                func.count(self.model_type.id),  # Считаем количество задач
                func.date(self.model_type.updated_at),
            )
            .where(
                self.model_type.user_id
                == user_id,  # Фильтруем по ID пользователя
                self.model_type.status
                == TaskStatus.done,  # Фильтруем по состоянию задачи
                (from_dt >= self.model_type.updated_at)
                & (
                    self.model_type.updated_at >= to_dt
                ),  # Фильтруем задачи, обновленные за период
            )
            .group_by(
                func.date(self.model_type.updated_at)
            )  # Группируем по дню обновления
        )
        result = await self.session.execute(stmt)
        return {date: count for count, date in result.all()}

    async def get_test_stats(self, user_id: UUID) -> dict[TestStatus, int]:
        stmt = (
            select(
                self.model_type.test_status,
                func.count(self.model_type.test_status),
            )
            .where(
                self.model_type.user_id == user_id,
                self.model_type.test_status != TestStatus.no_status,
            )
            .group_by(self.model_type.test_status)
        )
        result = await self.session.execute(stmt)
        return {status: count for status, count in result.all()}
