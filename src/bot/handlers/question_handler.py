import asyncio
import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import QuestionState
from bot.keyboards.moderation_kb import moderation_keyboard
from bot.states import StatesBot
from config import settings
from database.crud.questions import add_question_to_db, update_state

router = Router()


@router.message(StatesBot.INPUT_QUESTION, F.text)
async def get_message(message: Message, state: FSMContext, db_session: AsyncSession, bot: Bot):
    # get data for question object
    data = await state.get_data()
    competitor_id = data.get("contestant_id", 0)
    user_id = data.get("user_id", 0)

    messages_list = data.get("message_for_delete", [])
    for msg in messages_list:
        await bot.delete_message(chat_id=message.chat.id, message_id=msg)

    if not user_id or not competitor_id:
        logging.warning("User or contestant not found")
        return

    # add question to db
    question_id = await add_question_to_db(
        competitor_id=competitor_id,
        user_id=user_id,
        question=message.text,
        state=QuestionState.QUESTION,
        db_session=db_session,
    )

    by_msg = await message.answer("Спасибо за вопрос!")

    await message.delete()

    # send question to moderator
    await update_state(question_id=question_id, state=QuestionState.MODERATION, db_session=db_session)
    await bot.send_message(chat_id=settings.MODERATOR, text=message.text, reply_markup=moderation_keyboard(question_id))
    # out of state
    await state.set_state()

    await asyncio.sleep(5)
    await by_msg.delete()


@router.message(StatesBot.INPUT_QUESTION)
async def get_any_message(message: Message):
    await message.delete()
    msg_reply = await message.answer("Задайте свой вопрос текстом.")
    await asyncio.sleep(5)
    await msg_reply.delete()
