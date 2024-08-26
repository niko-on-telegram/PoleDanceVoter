from aiogram.filters.callback_data import CallbackData
from bot.enums import VoterEnum


class VoterCallbackFactory(CallbackData, prefix="voter"):
    user_id: int
    contestant_id: int
    action: VoterEnum
