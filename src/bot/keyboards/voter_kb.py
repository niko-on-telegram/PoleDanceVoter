from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.voter_factory import VoterCallbackFactory
from bot.enums import VoterEnum


def voter_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Проголосовать", callback_data=VoterCallbackFactory(tg_id=tg_id, action=VoterEnum.VOTE))
    kb.button(text="Назад", callback_data=VoterCallbackFactory(tg_id=tg_id, action=VoterEnum.BACK))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
