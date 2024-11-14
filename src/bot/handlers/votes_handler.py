import logging

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from magic_filter import F

from bot.callbacks.votes_factory import VotesCallbackFactory
from bot.enums import VotesEnum
from bot.keyboards.close_kb import CloseCallback

router = Router()


@router.callback_query(VotesCallbackFactory.filter(F.action == VotesEnum.BACK))
async def callback_back(
    callback: types.CallbackQuery,
):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        logging.info(f"Failed to delete message {callback.message.message_id}")
    await callback.answer()


@router.callback_query(CloseCallback.filter())
async def callback_back(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        logging.info(f"Failed to delete message {callback.message.message_id}")
    await state.set_state()
