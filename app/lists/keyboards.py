from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.base.pagination import Page
from app.lists.models import TodoList
from app.tasks.constants import TASK_STATUSES
from app.tasks.models import Task


def get_todo_list_kb(page: Page[TodoList]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in page.items:
        builder.row(
            InlineKeyboardButton(
                text=i.name,
                callback_data=f"show_todo_list:{i.id}",
            )
        )
    builder.adjust(1)
    builder.row(
        InlineKeyboardButton(text="Создать ➕", callback_data="add"),
    )
    return builder.as_markup(resize_keyboard=True)


def get_tasks_kb(
    tasks: Page[Task], *, action_btns: bool = True
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for task in tasks.items:
        builder.row(
            InlineKeyboardButton(
                text=f"{task.name} {TASK_STATUSES[task.status]['emoji']}",
                callback_data=f"show_task:{task.id}",
            )
        )
    if action_btns:
        builder.row(
            InlineKeyboardButton(text="Новая задача ➕", callback_data="add"),
            InlineKeyboardButton(
                text="Удалить список ❌", callback_data="delete"
            ),
        )
    builder.row(
        InlineKeyboardButton(text="Назад ⬅️", callback_data="to_todo_lists")
    )
    return builder.as_markup(resize_keyboard=True)
