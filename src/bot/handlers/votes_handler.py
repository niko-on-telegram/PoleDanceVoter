import asyncio

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InaccessibleMessage
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.plugin.plugin_base import logging

from bot.enums import VotesEnum, ContestantEnum
from bot.callbacks.votes_factory import VotesCallbackFactory
from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.handlers.contestant_handler import callback_profile
from bot.keyboards.close_kb import CloseCallback
from database.crud.contestant import inc_dec_vote_to_db as inc_dec_contestant_vote
from database.crud.user import inc_dec_vote_to_db as inc_dec_user_vote
from database.crud.votes import add_votes_to_db

router = Router()


@router.callback_query(VotesCallbackFactory.filter(F.action == VotesEnum.VOTE))
async def callback_vote(
        callback: types.CallbackQuery, callback_data: VotesCallbackFactory, db_session: AsyncSession
):
    if isinstance(callback.message, InaccessibleMessage):
        logging.debug("Caught inaccessible message")
        return
    await callback.message.delete()
    await inc_dec_contestant_vote(callback_data.contestant_id, db_session)
    await inc_dec_user_vote(callback.from_user.id, db_session)
    await add_votes_to_db(
        user_id=callback.from_user.id, competitor_id=callback_data.contestant_id, db_session=db_session
    )
    msg = await callback.message.answer("Спасибо за ваш голос!")
    await asyncio.sleep(5)
    await msg.delete()


@router.callback_query(VotesCallbackFactory.filter(F.action == VotesEnum.BACK))
async def callback_back(callback: types.CallbackQuery, callback_data: VotesCallbackFactory, db_session: AsyncSession,
                        state: FSMContext):
    await callback.message.delete()
    await callback.answer()


@router.callback_query(CloseCallback.filter())
async def callback_back(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state()
