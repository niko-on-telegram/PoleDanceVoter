from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.enums import ContestantEnum


def contestant_keyboard(user_id: int, contestant_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Проголосовать',
        callback_data=ContestantCallbackFactory(
            user_id=user_id, contestant_id=contestant_id, action=ContestantEnum.VOTE
        ),
    )
    kb.button(
        text='Задать вопрос',
        callback_data=ContestantCallbackFactory(
            user_id=user_id, contestant_id=contestant_id, action=ContestantEnum.QUESTION
        ),
    )
    kb.button(
        text='Посмотреть ответы',
        callback_data=ContestantCallbackFactory(
            user_id=user_id, contestant_id=contestant_id, action=ContestantEnum.CHECK_ANSWER
        ),
    )
    kb.button(
        text='К списку участников',
        callback_data=ContestantCallbackFactory(
            user_id=user_id, contestant_id=contestant_id, action=ContestantEnum.BACK
        ),
    )
    kb.adjust(1)
    return kb.as_markup()
