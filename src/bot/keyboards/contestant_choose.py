from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.enums import ContestantEnum


def contestant_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Проголосовать', callback_data=ContestantCallbackFactory(tg_id=tg_id, action=ContestantEnum.VOTE))
    kb.button(
        text='Задать вопрос', callback_data=ContestantCallbackFactory(tg_id=tg_id, action=ContestantEnum.QUESTION)
    )
    kb.button(
        text='Посмотреть ответы',
        callback_data=ContestantCallbackFactory(tg_id=tg_id, action=ContestantEnum.CHECK_ANSWER),
    )
    kb.adjust(1)
    return kb.as_markup()
