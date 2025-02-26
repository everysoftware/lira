import datetime
import os

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.db.utils import naive_utc
from app.stats.dependencies import StatsServiceDep
from app.users.dependencies import UserDep

router = Router()

# STATS


@router.message(Command("stats"))
@router.message(F.text == "Статистика 📊")
async def show(
    message: types.Message, user: UserDep, service: StatsServiceDep
) -> None:
    now = naive_utc()
    daily_stats_path = await service.plot_by_days(
        user.id, now, now - datetime.timedelta(days=365)
    )
    try:
        await message.answer_photo(
            photo=FSInputFile(daily_stats_path),
            caption="Статистика по задачам",
        )

    finally:
        os.remove(daily_stats_path)
