from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.crud.contestant import get_all_contestants, default_contestant


async def get_contestant_list(db_session) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    contestants = await get_all_contestants(db_session)
    if not contestants:
        contestants = default_contestant()

    for contestant in contestants:
        kb.row(types.InlineKeyboardButton(
            text=f'{contestant.fullname}      Голоса: {contestant.count_votes}', url="https://github.com")
        )
    return kb.as_markup(resize_keyboard=True)
