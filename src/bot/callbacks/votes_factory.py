from aiogram.filters.callback_data import CallbackData
from bot.enums import VotesEnum


class VotesCallbackFactory(CallbackData, prefix="votes"):
    user_id: int
    contestant_id: int
    action: VotesEnum
