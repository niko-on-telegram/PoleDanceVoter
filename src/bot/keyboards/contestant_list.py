from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Contestant
from bot.enums import ContestantEnum
from bot.callbacks.contestan_factory import ContestantCallbackFactory


def get_contestant_list(contestants: list[Contestant]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for contestant in contestants:
        kb.button(
            text=f'{contestant.fullname}     Голоса: {contestant.count_votes}',
            callback_data=ContestantCallbackFactory(tg_id=contestant.telegram_id, action=ContestantEnum.PROFILE),
        )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
