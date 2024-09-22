from aiogram.filters.callback_data import CallbackData


class ModerationCallbackFactory(CallbackData, prefix="moderation"):
    question_id: int
    state: int
