from aiogram.filters.callback_data import CallbackData

from bot.enums import QuestionBack


class QuestionBackCallback(CallbackData, prefix="question_back"):
    action: QuestionBack
