from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_contestant_from_db():
    return {"Снежанна": {"link": "https://github.com", "votes": 13},
            "Владислав": {"link": "https://github.com", "votes": 455},
            "Педро": {"link": "https://github.com", "votes": 666},
            "Анжелика": {"link": "https://github.com", "votes": 134},
            "Гоги": {"link": "https://github.com", "votes": 12},
            "Рикардо": {"link": "https://github.com", "votes": 999},
            "Белатриса": {"link": "https://github.com", "votes": 132},
            "Кирилл": {"link": "https://github.com", "votes": 143},
            "Анна": {"link": "https://github.com", "votes": 12},
            "Зульфия": {"link": "https://github.com", "votes": 16}
            }


def get_contestant_list() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for name, data in get_contestant_from_db().items():
        kb.row(types.InlineKeyboardButton(
            text=f'{name}      Голоса: {data["votes"]}', url=data["link"])
        )

    return kb.as_markup(resize_keyboard=True)
