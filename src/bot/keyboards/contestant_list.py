from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Competitor
from bot.enums import ContestantEnum
from bot.callbacks.contestant_factory import ContestantCallbackFactory


def get_contestant_list(contestants: list[Competitor]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for contestant in contestants:
        kb.button(
            text=f'{contestant.full_name}',
            callback_data=ContestantCallbackFactory(
                contestant_id=contestant.telegram_id, action=ContestantEnum.PROFILE
            ),
        )
    kb.adjust(1)
    return kb.as_markup()
