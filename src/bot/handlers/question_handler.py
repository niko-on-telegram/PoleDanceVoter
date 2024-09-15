from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaVideo
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.question_back import QuestionBackCallback
from bot.enums import QuestionState, QuestionBack
from bot.keyboards.contestant_choose import contestant_keyboard
from bot.keyboards.contestant_question_kb import question_error_user_keyboard
from bot.keyboards.moderation_kb import moderation_keyboard
from bot.states import StatesBot
from config import settings
from database.crud.contestant import get_contestant_from_db
from database.crud.questions import add_question_to_db, update_state

router = Router()


@router.message(StatesBot.INPUT_QUESTION, F.text)
async def get_message(message: Message, state: FSMContext, db_session: AsyncSession, bot: Bot):
    # get data for question object
    data = await state.get_data()
    contestant_id = data.get("contestant_id", 0)
    user_id = data.get("user_id", 0)
    if not user_id or not contestant_id:
        return

    # add question to db
    question_id = await add_question_to_db(
        contestant_id=contestant_id,
        user_id=user_id,
        question=message.text,
        state=QuestionState.QUESTION,
        db_session=db_session,
    )

    by_msg = await message.answer("Спасибо за вопрос!")

    # delete messages
    messages = data.get("message_for_delete", [])
    await state.update_data(message_for_delete=[], question_id=question_id)
    for msg in messages:
        await bot.delete_message(chat_id=by_msg.chat.id, message_id=msg)

    await bot.delete_message(chat_id=by_msg.chat.id, message_id=by_msg.message_id)

    # send question to moderator
    await update_state(question_id=question_id, state=QuestionState.MODERATION, db_session=db_session)
    await bot.send_message(chat_id=settings.MODERATOR, text=message.text, reply_markup=moderation_keyboard(question_id))
    # out from state
    await state.clear()
    # print profile contestant
    await print_profile(contestant_id, user_id, db_session, bot)


async def print_profile(contestant_id: int, user_id: int, db_session: AsyncSession, bot: Bot):
    contestant = await get_contestant_from_db(contestant_id, db_session)
    message_list = await bot.send_media_group(
        chat_id=user_id,
        protect_content=True,
        media=[
            InputMediaVideo(media=contestant.video_first),
            InputMediaVideo(media=contestant.video_second),
            InputMediaVideo(media=contestant.video_third),
        ],
    )
    await bot.send_message(
        chat_id=user_id,
        text=contestant.description,
        reply_markup=contestant_keyboard(
            user_id=user_id,
            contestant_id=contestant_id,
            video1_id=message_list[0].message_id,
            video2_id=message_list[1].message_id,
            video3_id=message_list[2].message_id,
            chat_id=message_list[0].chat.id,
        ),
    )


@router.message(StatesBot.INPUT_QUESTION)
async def get_any_message(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = await message.answer("Вы ввели не текст! Введите только текст.", reply_markup=question_error_user_keyboard())
    messages = data.get("message_for_delete", [])
    messages.append(msg.message_id)
    messages.append(message.message_id)
    await state.update_data(message_for_delete=messages)
    return


@router.message(QuestionBackCallback.filter(F.action == QuestionBack.BACK))
async def get_message(message: Message, state: FSMContext, db_session: AsyncSession, bot: Bot):
    # get data for question object
    data = await state.get_data()
    contestant_id = data.get("contestant_id", 0)
    user_id = data.get("user_id", 0)
    if not user_id or not contestant_id:
        return

    await message.delete()

    # delete messages
    messages = data.get("message_for_delete", [])
    await state.update_data(message_for_delete=[])
    for msg in messages:
        await bot.delete_message(chat_id=user_id, message_id=msg)

    # out from state
    await state.clear()
    # print profile contestant
    await print_profile(contestant_id, user_id, db_session, bot)

