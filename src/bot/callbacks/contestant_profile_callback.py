from aiogram.filters.callback_data import CallbackData
from bot.enums import ContestantEnum


class ContestantProfileCallbackFactory(CallbackData, prefix="profile"):
    user_id: int
    contestant_id: int
    action: ContestantEnum
    video1_id: int
    video2_id: int
    video3_id: int
    chat_id: int
