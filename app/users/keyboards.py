from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Задачи ✅"),
            KeyboardButton(text="Списки 📝"),
        ],
        [
            KeyboardButton(text="Статистика 📊"),
            KeyboardButton(text="Помощь 🧭"),
        ],
        [
            KeyboardButton(text="Сменить пространство 📦"),
        ],
    ],
    resize_keyboard=True,
)
