from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_contestant() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text=f'Проголосовать', callback_data="Contestant_vote"))
    kb.row(types.InlineKeyboardButton(text=f'Задать вопрос', callback_data="Contestant_question"))
    kb.row(types.InlineKeyboardButton(text=f'Посмотреть ответы', callback_data="Contestant_check_answers"))
    return kb.as_markup(resize_keyboard=True)
