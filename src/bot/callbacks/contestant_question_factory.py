from aiogram.filters.callback_data import CallbackData


class ContestantQuestionCallbackFactory(CallbackData, prefix="contestant_question"):
    question_id: int
    state: int
