import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.callbacks.contestant_profile_callback import ContestantProfileCallbackFactory
from bot.enums import ContestantEnum
from bot.helpers import print_constestant_list, print_profile
from bot.keyboards.close_kb import close_keyboard
from bot.keyboards.contestant_choose import contestant_keyboard_ok
from bot.keyboards.votes_kb import votes_keyboard
from bot.states import StatesBot
from database.crud.contestant import get_competitor_from_db
from database.crud.questions import get_all_questions
from database.crud.votes import get_all_votes_ids
from database.models import User

router = Router()


async def delete_message_video(callback: types.CallbackQuery, chat_id: int, msg_list: list[int]):
    for msg_id in msg_list:
        logging.debug(f"{chat_id=} {msg_id=}")
        await callback.bot.delete_message(chat_id=chat_id, message_id=msg_id)


# noinspection PyTypeChecker
@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.DELETE))
async def callback_delete(
    callback: types.CallbackQuery, callback_data: ContestantCallbackFactory, db_session: AsyncSession, state: FSMContext
):
    await callback.message.delete()


@router.callback_query(ContestantProfileCallbackFactory.filter(F.action == ContestantEnum.BACK))
async def callback_back(callback: types.CallbackQuery, db_session: AsyncSession, user: User, state: FSMContext):
    data = await state.get_data()
    msg_ids = data.get('msg_ids', [])
    await delete_message_video(callback=callback, chat_id=callback.from_user.id, msg_list=msg_ids)

    await print_constestant_list(message=callback.message, db_session=db_session)
    await state.clear()


@router.callback_query(ContestantProfileCallbackFactory.filter(F.action == ContestantEnum.VOTE))
async def callback_vote(
    callback: types.CallbackQuery,
    callback_data: ContestantProfileCallbackFactory,
    db_session: AsyncSession,
    user: User,
):
    if user.count_votes >= 3:
        await callback.answer(text="Вы уже проголосовали допустимое количество раз!")
        return

    voters = await get_all_votes_ids(user.telegram_id, db_session)
    for voter in voters:
        if voter.competitor_id == callback_data.contestant_id:
            await callback.answer(text="Вы уже голосовали за этого участника!")
            return

    contestant = await get_competitor_from_db(callback_data.contestant_id, db_session)
    await callback.message.answer(
        text=f"Вы уверены что хотите проголосовать за участника {contestant.full_name}?",
        reply_markup=votes_keyboard(contestant_id=contestant.telegram_id),
    )
    await callback.answer()


# noinspection PyTypeChecker
@router.callback_query(ContestantCallbackFactory.filter(F.action == ContestantEnum.PROFILE))
async def callback_profile(
    callback: types.CallbackQuery, callback_data: ContestantCallbackFactory, db_session: AsyncSession, state: FSMContext
):
    await callback.message.delete()
    await print_profile(callback.message, callback_data.contestant_id, db_session, state)


# noinspection PyTypeChecker
@router.callback_query(ContestantProfileCallbackFactory.filter(F.action == ContestantEnum.CHECK_ANSWER))
async def callback_check_answer(
    callback: types.CallbackQuery,
    callback_data: ContestantProfileCallbackFactory,
    db_session: AsyncSession,
    state: FSMContext,
):
    questions = await get_all_questions(callback_data.contestant_id, db_session)
    contestant = await get_competitor_from_db(callback_data.contestant_id, db_session)
    if not questions:
        question_txt = f"Участнику {contestant.full_name} ещё не задали вопросов."
    else:
        question_txt = f"Вопросы для {contestant.full_name}:\n\n"
        for question in questions:
            question_txt += f"- {question}\n\n"

    await callback.message.answer(
        text=question_txt,
        reply_markup=contestant_keyboard_ok(contestant_id=callback_data.contestant_id),
    )
    await callback.answer()


# noinspection PyTypeChecker
@router.callback_query(ContestantProfileCallbackFactory.filter(F.action == ContestantEnum.QUESTION))
async def callback_question(
    callback: types.CallbackQuery,
    callback_data: ContestantProfileCallbackFactory,
    db_session: AsyncSession,
    user: User,
    state: FSMContext,
):
    contestant = await get_competitor_from_db(callback_data.contestant_id, db_session)
    msg = await callback.message.answer(text=f"Напишите вопрос для {contestant.full_name}, только текст.", reply_markup=close_keyboard())

    data = await state.get_data()
    messages = data.get("message_for_delete", [])
    messages.append(msg.message_id)
    await state.update_data(message_for_delete=messages, user_id=user.telegram_id, contestant_id=contestant.telegram_id)
    await callback.answer()
    await state.set_state(StatesBot.INPUT_QUESTION)
