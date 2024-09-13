from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.contestant_question_factory import ContestantQuestionCallbackFactory
from bot.enums import QuestionState


def question_keyboard(question_id: int) -> InlineKeyboardMarkup:
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


def question_error_keyboard(question_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Отклонить вопрос",
        callback_data=ContestantQuestionCallbackFactory(question_id=question_id, state=QuestionState.REJECTED),
    )
    kb.adjust(1)
    return kb.as_markup()
