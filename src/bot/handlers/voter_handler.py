from aiogram import Router, types
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import VoterEnum, ContestantEnum
from bot.callbacks.voter_factory import VoterCallbackFactory
from bot.callbacks.contestan_factory import ContestantCallbackFactory
from bot.handlers.contestant_handler import callback_profile
from database.crud.contestant import inc_dec_vote_to_db as inc_dec_contestant_vote
from database.crud.user import inc_dec_vote_to_db as inc_dec_user_vote, get_user_from_db_by_tg_id

router = Router()


@router.callback_query(VoterCallbackFactory.filter(F.action == VoterEnum.VOTE))
async def callback_check_answer(
    callback: types.CallbackQuery, callback_data: VoterCallbackFactory, db_session: AsyncSession
):
    user = await get_user_from_db_by_tg_id(callback_data.tg_id, db_session)
    if user.count_votes > 3:
        await callback.answer(text="Вы уже проголосовали допустимое количество раз!")
    #TODO: проверить что за этого участника этот пользователь уже проголосовал
    await inc_dec_contestant_vote(callback_data.tg_id, db_session)
    await inc_dec_user_vote(callback_data.tg_id, db_session)
    await callback.answer("Спасибо за ваш голос!")


@router.callback_query(VoterCallbackFactory.filter(F.action == VoterEnum.BACK))
async def callback_check_answer(
    callback: types.CallbackQuery, callback_data: VoterCallbackFactory, db_session: AsyncSession
):
    await callback_profile(
        callback, ContestantCallbackFactory(tg_id=callback_data.tg_id, action=ContestantEnum.PROFILE), db_session
    )
    await callback.answer()
