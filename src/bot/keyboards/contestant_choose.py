from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.callbacks.contestant_profile_callback import ContestantProfileCallbackFactory
from bot.enums import ContestantEnum


def contestant_keyboard(contestant_id: int, already_voted: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Задать вопрос',
        callback_data=ContestantProfileCallbackFactory(contestant_id=contestant_id, action=ContestantEnum.QUESTION),
    )
    kb.button(
        text='Посмотреть ответы',
        callback_data=ContestantProfileCallbackFactory(contestant_id=contestant_id, action=ContestantEnum.CHECK_ANSWER),
    )
    kb.button(
        text='К списку участников',
        callback_data=ContestantProfileCallbackFactory(contestant_id=contestant_id, action=ContestantEnum.BACK),
    )
    kb.adjust(1)
    return kb.as_markup()


def contestant_keyboard_ok(contestant_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Закрыть',
        callback_data=ContestantCallbackFactory(contestant_id=contestant_id, action=ContestantEnum.DELETE),
    )
    return kb.as_markup()
