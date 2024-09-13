from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callbacks.moderation_factory import ModerationCallbackFactory
from bot.enums import QuestionState


def moderation_keyboard(question_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Отправить участнику",
        callback_data=ModerationCallbackFactory(question_id=question_id, state=QuestionState.WAITING_RESPONSE),
    )
    kb.button(
        text="Отклонить",
        callback_data=ModerationCallbackFactory(question_id=question_id, state=QuestionState.REJECTED),
    )
    kb.adjust(1)
    return kb.as_markup()
