from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CloseCallback(CallbackData, prefix="close_and_thats_it"):
    pass


def close_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Закрыть",
        callback_data=CloseCallback().pack(),
    )
    kb.adjust(1)
    return kb.as_markup()
