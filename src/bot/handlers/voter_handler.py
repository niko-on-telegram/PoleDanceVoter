from aiogram import Router, types
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import VoterEnum, ContestantEnum
from bot.callbacks.voter_factory import VoterCallbackFactory
from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.handlers.contestant_handler import callback_back as back_to_contestants, callback_profile
from database.crud.contestant import inc_dec_vote_to_db as inc_dec_contestant_vote
from database.crud.user import inc_dec_vote_to_db as inc_dec_user_vote, get_user_from_db_by_tg_id
from database.crud.voter import get_all_voter_ids, add_voter_to_db

from database.models import User

router = Router()


@router.callback_query(VoterCallbackFactory.filter(F.action == VoterEnum.VOTE))
async def callback_vote(callback: types.CallbackQuery, callback_data: VoterCallbackFactory, db_session: AsyncSession):
    fab = ContestantCallbackFactory(
        user_id=callback_data.user_id, contestant_id=callback_data.contestant_id, action=ContestantEnum.BACK
    )
    user = await get_user_from_db_by_tg_id(callback_data.user_id, db_session)
    if user.count_votes >= 3:
        await callback.answer(text="Вы уже проголосовали допустимое количество раз!")
        await back_to_contestants(callback=callback, callback_data=fab, db_session=db_session, user=user)
        return

    voters = await get_all_voter_ids(callback_data.user_id, db_session)
    for voter in voters:
        if voter.contestant_id == callback_data.contestant_id:
            await callback.answer(text="Вы уже голосовали за этого участника!")
            await back_to_contestants(callback=callback, callback_data=fab, db_session=db_session, user=user)
            return

    await inc_dec_contestant_vote(callback_data.contestant_id, db_session)
    await inc_dec_user_vote(callback_data.user_id, db_session)
    await add_voter_to_db(
        user_id=callback_data.user_id, contestant_id=callback_data.contestant_id, db_session=db_session
    )
    await callback.answer("Спасибо за ваш голос!")
    await back_to_contestants(callback=callback, callback_data=fab, db_session=db_session, user=user)


@router.callback_query(VoterCallbackFactory.filter(F.action == VoterEnum.BACK))
async def callback_check_answer(
    callback: types.CallbackQuery, callback_data: VoterCallbackFactory, db_session: AsyncSession
):
    await callback_profile(
        callback,
        ContestantCallbackFactory(
            user_id=callback_data.user_id, contestant_id=callback_data.contestant_id, action=ContestantEnum.PROFILE
        ),
        db_session,
    )
    await callback.answer()
