from aiogram.filters.callback_data import CallbackData
from bot.enums import ContestantEnum


class ContestantCallbackFactory(CallbackData, prefix="contestant"):
    user_id: int
    contestant_id: int
    action: ContestantEnum
