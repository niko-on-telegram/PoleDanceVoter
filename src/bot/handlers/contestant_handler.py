from aiogram import Router, types
from aiogram.types import InputMediaVideo
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.contestant_choose import contestant_keyboard
from bot.callbacks.contestant_factory import ContestantCallbackFactory
from magic_filter import F

from bot.enums import ContestantEnum
from database.crud.user import get_user_from_db_by_tg_id
from database.crud.votes import get_all_votes_ids
from database.models import User
from bot.internal.hello_img import hello_img
from bot.keyboards.contestant_list import get_contestant_list
from bot.keyboards.votes_kb import votes_keyboard
from database.crud.contestant import get_contestant_from_db, get_all_contestants

router = Router()


@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.BACK))
async def callback_back(
    callback: types.CallbackQuery, callback_data: ContestantCallbackFactory, db_session: AsyncSession, user: User
):
    contestants = await get_all_contestants(db_session)
    await callback.message.answer_photo(
        photo=hello_img,
        caption=f'{user.full_name}, список участников:',
        reply_markup=get_contestant_list(contestants, callback_data.user_id),
    )
    await callback.answer()


@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.CHECK_ANSWER))
async def callback_check_answer(callback: types.CallbackQuery, callback_data: ContestantCallbackFactory):
    await callback.message.answer(text=f"Check answer {callback_data.user_id}")
    await callback.answer()


@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.QUESTION))
async def callback_question(callback: types.CallbackQuery, callback_data: ContestantCallbackFactory):
    await callback.message.answer(text=f"Question {callback_data.user_id}")
    await callback.answer()


@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.VOTE))
async def callback_vote(
    callback: types.CallbackQuery, callback_data: ContestantCallbackFactory, db_session: AsyncSession
):
    user = await get_user_from_db_by_tg_id(callback_data.user_id, db_session)
    if user.count_votes >= 3:
        await callback.answer(text="Вы уже проголосовали допустимое количество раз!")
        return

    voters = await get_all_votes_ids(callback_data.user_id, db_session)
    for voter in voters:
        if voter.contestant_id == callback_data.contestant_id:
            await callback.answer(text="Вы уже голосовали за этого участника!")
            return

    contestant = await get_contestant_from_db(callback_data.contestant_id, db_session)
    await callback.message.answer(
        text=f"Вы уверены что хотите проголосовать за участника {contestant.full_name}?",
        reply_markup=votes_keyboard(user_id=callback_data.user_id, contestant_id=contestant.telegram_id),
    )
    await callback.answer()


@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.PROFILE))
async def callback_profile(
    callback: types.CallbackQuery, callback_data: ContestantCallbackFactory, db_session: AsyncSession
):
    contestant = await get_contestant_from_db(callback_data.contestant_id, db_session)
    await callback.message.answer_media_group(
        protect_content=True,
        media=[
            InputMediaVideo(media=contestant.video_first),
            InputMediaVideo(media=contestant.video_second),
            InputMediaVideo(media=contestant.video_third),
        ],
    )
    await callback.message.answer(
        text=contestant.description,
        reply_markup=contestant_keyboard(user_id=callback_data.user_id, contestant_id=callback_data.contestant_id),
    )
    await callback.answer()
