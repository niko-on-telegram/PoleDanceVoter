from aiogram.filters.callback_data import CallbackData

from bot.enums import ContestantEnum


class ContestantCallbackFactory(CallbackData, prefix="contestant"):
    contestant_id: int
    action: ContestantEnum
