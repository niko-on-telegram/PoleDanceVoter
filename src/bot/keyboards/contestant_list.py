from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Contenstant


async def get_contestant_list(contestants: list[Contenstant]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for contestant in contestants:
        kb.row(types.InlineKeyboardButton(
            text=f'{contestant.fullname}     Голоса: {contestant.count_votes}',
            url="https://github.com")
        )
    return kb.as_markup(resize_keyboard=True)
