from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ContestantCallbackFactory(CallbackData, prefix="contestant"):
    value: Optional[int] = None
