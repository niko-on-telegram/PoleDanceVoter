from aiogram.filters.callback_data import CallbackData
from bot.enums import VoterEnum


class VoterCallbackFactory(CallbackData, prefix="voter"):
    tg_id: int
    action: VoterEnum
