from aiogram.filters.callback_data import CallbackData
from bot.enums import ContestantEnum


class ContestantProfileCallbackFactory(CallbackData, prefix="profile"):
    contestant_id: int
    action: ContestantEnum
