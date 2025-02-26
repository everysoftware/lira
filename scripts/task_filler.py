import asyncio
import datetime
import logging
import random
from typing import Sequence, Any

import numpy as np
import pandas as pd
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.base.types import UUID, naive_utc
from app.lists.models import TodoList
from app.tasks.models import Task
from app.tasks.schemas import TaskStatus, TestStatus
from app.users.models import User
from app.workspaces.models import Workspace


def generate_timestamps(number: int) -> Sequence[datetime.datetime]:
    now = naive_utc()
    timestamps = np.random.choice(
        pd.date_range(
            start=now - datetime.timedelta(days=365 - 30), end=now, freq="D"
        ),
        number,
    )
    logging.info("Generated %d timestamps", number)
    return timestamps


def get_test_status(passed_p: float) -> TestStatus:
    if random.random() < passed_p:
        return TestStatus.passed
    return random.choice([s for s in TestStatus if s != TestStatus.passed])


def generate_statuses(
    number: int, *, done_p: float, test_p: float, passed_p: float
) -> tuple[Sequence[TaskStatus], Sequence[TestStatus]]:
    statuses = [TaskStatus.to_do for _ in range(number)]
    test_statuses = [TestStatus.no_status for _ in range(number)]

    done_count = int(number * done_p)
    done_indices = random.sample(range(number), done_count)

    for i in done_indices:
        statuses[i] = TaskStatus.done
        if random.random() < test_p:
            test_statuses[i] = get_test_status(passed_p)
    logging.info("Generated %d statuses (%d done)", number, done_count)
    return statuses, test_statuses


def get_df(number: int, **static: Any) -> pd.DataFrame:
    timestamps = generate_timestamps(number)
    statuses, test_statuses = generate_statuses(
        number, done_p=0.9, test_p=0.8, passed_p=0.6
    )
    df = pd.DataFrame(
        {
            "name": "Test",
            "created_at": timestamps,
            "updated_at": timestamps,
            "status": statuses,
            "test_status": test_statuses,
            **static,
        }
    )
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    return df


async def fill_tasks_table(db_url: str, user_id: UUID, number: int) -> None:
    engine = create_async_engine(
        db_url,
        echo=False,
        pool_pre_ping=True,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        async with session.begin():
            user: User = await session.get_one(User, user_id)  # noqa
            ws = Workspace(name="Test workspace", user=user)
            project = TodoList(name="Test list", user=user, workspace=ws)
            session.add_all((ws, project))
            await session.flush()
            df = get_df(
                number,
                user_id=user.id,
                workspace_id=ws.id,
                todo_list_id=project.id,
            )
            stmt = insert(Task)
            await session.execute(stmt, df.to_dict(orient="records"))
    logging.info("Filled tasks table with %d tasks", number)


def get_valid_integer(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    db_url = input(
        "Enter DB url (e.g. postgresql+asyncpg://postgres:changethis@db:5432/app): "
    )
    user_id = input(
        "Enter user ID (e.g. 3a2ec830-c4d5-465a-8a22-09bb302b58fa): "
    )
    number = get_valid_integer("Enter number of tasks (e.g. 1000): ")
    await fill_tasks_table(db_url, user_id, number)  # type: ignore[call-arg]
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
