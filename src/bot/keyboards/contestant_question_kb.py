from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.contestant_question_factory import ContestantQuestionCallbackFactory
from bot.callbacks.question_back import QuestionBackCallback
from bot.enums import QuestionState, QuestionBack


def question_keyboard(
    question_id: int,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Ответить на вопрос",
        callback_data=ContestantQuestionCallbackFactory(question_id=question_id, state=QuestionState.WAITING_RESPONSE),
    )
    kb.button(
        text="Отклонить вопрос",
        callback_data=ContestantQuestionCallbackFactory(question_id=question_id, state=QuestionState.REJECTED),
    )
    kb.adjust(1)
    return kb.as_markup()


def question_reject_keyboard(question_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Отклонить вопрос",
        callback_data=ContestantQuestionCallbackFactory(question_id=question_id, state=QuestionState.REJECTED),
    )
    kb.adjust(1)
    return kb.as_markup()


def question_error_user_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="К профилю",
        callback_data=QuestionBackCallback(action=QuestionBack.BACK),
    )
    kb.adjust(1)
    return kb.as_markup()
