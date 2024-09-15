from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.contestant_question_factory import ContestantQuestionCallbackFactory
from bot.enums import QuestionState
from bot.keyboards.contestant_question_kb import  question_error_keyboard
from bot.states import StatesBot
from database.crud.questions import update_state, get_question, add_answer_to_db

router = Router()


@router.callback_query(ContestantQuestionCallbackFactory.filter(F.state == QuestionState.WAITING_RESPONSE))
async def waiting_response_callback(
    callback: types.CallbackQuery,
    callback_data: ContestantQuestionCallbackFactory,
    bot: Bot,
    state: FSMContext,
    db_session: AsyncSession,
):
    chat_id = callback.message.chat.id
    await callback.message.delete()
    data = await state.get_data()
    question_id = callback_data.question_id
    question = await get_question(question_id=question_id, db_session=db_session)

    msg = await bot.send_message(
        chat_id=chat_id,
        text=f"Введите ответ на вопрос \"{question.question}\"текстом:",
        reply_markup=question_error_keyboard(question_id=question_id),
    )
    messages_list = data.get("message_for_delete", [])
    messages_list.append(msg.message_id)
    await state.update_data(
        message_for_delete=messages_list,
        contestant_id=question.contestant_id,
        user_id=question.user_id,
        question_id=question_id,
    )
    await state.set_state(StatesBot.ANSWER_QUESTION)


@router.callback_query(ContestantQuestionCallbackFactory.filter(F.state == QuestionState.REJECTED))
async def reject_callback(
    callback: types.CallbackQuery,
    callback_data: ContestantQuestionCallbackFactory,
    db_session: AsyncSession,
    state: FSMContext,
    bot: Bot,
):
    data = await state.get_data()
    messages_list = data.get("message_for_delete", [])
    if not messages_list:
        await callback.message.delete()
    await state.update_data(message_for_delete=[])
    for msg in messages_list:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg)


    await update_state(question_id=callback_data.question_id, state=QuestionState.REJECTED, db_session=db_session)
    await callback.answer("Вопрос отклонён")
    await state.clear()


@router.message(StatesBot.ANSWER_QUESTION, F.text)
async def get_message(message: Message, state: FSMContext, db_session: AsyncSession, bot: Bot):
    # get data for question object
    data = await state.get_data()
    user_id = data.get("user_id", 0)
    if not user_id:
        return

    question_id = data.get("question_id")
    await add_answer_to_db(question_id=question_id, db_session=db_session, answer=message.text)
    await update_state(question_id=question_id, state=QuestionState.ANSWERED, db_session=db_session)

    by_msg = await message.answer("Спасибо за ответ!")

    # delete messages
    messages_list = data.get("message_for_delete", [])
    await state.update_data(message_for_delete=[])
    for msg in messages_list:
        await bot.delete_message(chat_id=by_msg.chat.id, message_id=msg)

    await bot.delete_message(chat_id=by_msg.chat.id, message_id=by_msg.message_id)
    await message.delete()
    # out from state
    await state.clear()


@router.message(StatesBot.ANSWER_QUESTION)
async def get_any_message(message: Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get("question_id")
    msg = await message.answer(
        "Вы ввели не текст! Ответ должен состоять из текста. Введите ответ еще раз:",
        reply_markup=question_error_keyboard(question_id=question_id),
    )
    messages_list = data.get("message_for_delete", [])
    messages_list.append(msg.message_id)
    messages_list.append(message.message_id)
    await state.update_data(message_for_delete=messages_list)
    return
