from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.votes_factory import VotesCallbackFactory
from bot.enums import VotesEnum


def votes_keyboard(user_id: int, contestant_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Проголосовать",
        callback_data=VotesCallbackFactory(user_id=user_id, contestant_id=contestant_id, action=VotesEnum.VOTE),
    )
    kb.button(
        text="Назад",
        callback_data=VotesCallbackFactory(user_id=user_id, contestant_id=contestant_id, action=VotesEnum.BACK),
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
