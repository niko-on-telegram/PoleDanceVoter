import asyncio
import logging

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InaccessibleMessage
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import VotesEnum, ContestantEnum
from bot.callbacks.votes_factory import VotesCallbackFactory
from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.handlers.contestant_handler import callback_profile
from bot.keyboards.close_kb import CloseCallback
from database.crud.contestant import inc_dec_vote_to_db as inc_dec_contestant_vote
from database.crud.user import inc_dec_vote_to_db as inc_dec_user_vote
from database.crud.votes import add_votes_to_db

router = Router()


@router.callback_query(VotesCallbackFactory.filter(F.action == VotesEnum.BACK))
async def callback_back(
    callback: types.CallbackQuery
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
