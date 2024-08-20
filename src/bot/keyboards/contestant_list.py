from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_contestant_from_db():
    return {"1": "https://github.com",
            "2": "https://github.com",
            "3": "https://github.com",
            "4": "https://github.com",
            "5": "https://github.com",
            "6": "https://github.com",
            "7": "https://github.com",
            "8": "https://github.com",
            "9": "https://github.com",
            "10": "https://github.com"
            }


def get_contestant_list() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for name, link in get_contestant_from_db().items():
        kb.row(types.InlineKeyboardButton(
            text=name, url=link)
        )

    return kb.as_markup(resize_keyboard=True)
