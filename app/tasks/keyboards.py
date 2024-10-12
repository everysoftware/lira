from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.schemas import Page
from app.tasks.constants import TASK_STATUSES, TEST_STATUSES
from app.tasks.schemas import TaskRead


def get_status_kb(
    statuses: dict[Any, dict[str, Any]], *, cb_prefix: str
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for status in statuses.values():
        builder.row(
            InlineKeyboardButton(
                text=f"{status["text"]} {status["emoji"]}",
                callback_data=f"{cb_prefix}:{status["name"]}",
            )
        )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


EDIT_TASK_STATUS_KB = get_status_kb(TASK_STATUSES, cb_prefix="set_status")
EDIT_TEST_STATUS_KB = get_status_kb(TEST_STATUSES, cb_prefix="set_test_status")

SHOW_TASK_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️", callback_data="edit_status"),
            InlineKeyboardButton(text="🧪", callback_data="edit_test_status"),
            InlineKeyboardButton(text="💬", callback_data="comment"),
            InlineKeyboardButton(text="🔗", callback_data="report"),
            InlineKeyboardButton(text="❌", callback_data="delete"),
        ],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="to_checklist")],
    ]
)


def get_tasks_kb(
    tasks: Page[TaskRead], *, action_btns: bool = True
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
            InlineKeyboardButton(
                text="Создать задачу ➕", callback_data="add"
            ),
            InlineKeyboardButton(
                text="Удалить чек-лист ❌", callback_data="delete"
            ),
        )
    builder.row(
        InlineKeyboardButton(text="Назад ⬅️", callback_data="to_checklists")
    )
    return builder.as_markup(resize_keyboard=True)
