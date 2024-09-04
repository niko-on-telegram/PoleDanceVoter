from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.callbacks.contestant_profile_callback import ContestantProfileCallbackFactory
from bot.enums import ContestantEnum


def contestant_keyboard(
    user_id: int, contestant_id: int, video1_id: int, video2_id: int, video3_id: int, chat_id: int
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Проголосовать',
        callback_data=ContestantProfileCallbackFactory(
            user_id=user_id,
            contestant_id=contestant_id,
            action=ContestantEnum.VOTE,
            video1_id=video1_id,
            video2_id=video2_id,
            video3_id=video3_id,
            chat_id=chat_id,
        ),
    )
    kb.button(
        text='Задать вопрос',
        callback_data=ContestantProfileCallbackFactory(
            user_id=user_id,
            contestant_id=contestant_id,
            action=ContestantEnum.QUESTION,
            video1_id=video1_id,
            video2_id=video2_id,
            video3_id=video3_id,
            chat_id=chat_id,
        ),
    )
    kb.button(
        text='Посмотреть ответы',
        callback_data=ContestantProfileCallbackFactory(
            user_id=user_id,
            contestant_id=contestant_id,
            action=ContestantEnum.CHECK_ANSWER,
            video1_id=video1_id,
            video2_id=video2_id,
            video3_id=video3_id,
            chat_id=chat_id,
        ),
    )
    kb.button(
        text='К списку участников',
        callback_data=ContestantProfileCallbackFactory(
            user_id=user_id,
            contestant_id=contestant_id,
            action=ContestantEnum.BACK,
            video1_id=video1_id,
            video2_id=video2_id,
            video3_id=video3_id,
            chat_id=chat_id,
        ),
    )
    kb.adjust(1)
    return kb.as_markup()


def contestant_keyboard_ok(user_id: int, contestant_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Закрыть',
        callback_data=ContestantCallbackFactory(
            user_id=user_id, contestant_id=contestant_id, action=ContestantEnum.DELETE
        ),
    )
    return kb.as_markup()
