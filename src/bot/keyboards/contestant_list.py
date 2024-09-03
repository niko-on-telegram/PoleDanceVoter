from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Contestant
from bot.enums import ContestantEnum
from bot.callbacks.contestant_factory import ContestantCallbackFactory


def get_contestant_list(contestants: list[Contestant], user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for contestant in contestants:
        kb.button(
            text=f'{contestant.full_name}     Голоса: {contestant.count_votes}',
            callback_data=ContestantCallbackFactory(
                contestant_id=contestant.telegram_id, user_id=user_id, action=ContestantEnum.PROFILE
            ),
        )
    kb.adjust(1)
    return kb.as_markup()
