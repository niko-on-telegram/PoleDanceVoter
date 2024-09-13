from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaVideo
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import QuestionState
from bot.keyboards.contestant_choose import contestant_keyboard
from bot.keyboards.contestant_question_kb import question_keyboard
from bot.states import StatesBot
from config import settings
from database.crud.contestant import get_contestant_from_db
from database.crud.questions import add_question_to_db

router = Router()


@router.message(StatesBot.INPUT_QUESTION, F.text)
async def get_message(message: Message, state: FSMContext, db_session: AsyncSession, bot: Bot):
    # get data for question object
    data = await state.get_data()
    contestant_id = data.get("contestant_id", 0)
    user_id = data.get("user_id", 0)
    if not data or not contestant_id:
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
    await state.update_data(message_for_delete=[])
    for msg in messages:
        await bot.delete_message(chat_id=by_msg.chat_id, message_id=msg)

    await bot.delete_message(chat_id=by_msg.chat_id, message_id=by_msg.message_id)

    # send question to moderator
    await bot.send_message(chat_id=settings.MODERATOR, text=message.text, reply_markup=question_keyboard(question_id))

    # print profile contestant
    await print_profile(contestant_id, user_id, db_session, bot)

    # out from state
    await state.clear()


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
    msg = await message.answer("Вы ввели не текст! Введите только текст.")
    data = await state.get_data()
    messages = data.get("message_for_delete", [])
    messages.append(msg.id)
    messages.append(message.id)
    await state.update_data(message_for_delete=messages)
    return
