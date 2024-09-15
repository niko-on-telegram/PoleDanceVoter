from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.contestant_question_factory import ContestantQuestionCallbackFactory
from bot.enums import QuestionState
from bot.keyboards.contestant_question_kb import question_keyboard
from bot.states import StatesBot
from database.crud.questions import update_state

router = Router()


@router.callback_query(ContestantQuestionCallbackFactory.filter(F.action == QuestionState.WAITING_RESPONSE))
async def waiting_response_callback(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    chat_id = callback.message.chat_id
    await callback.message.delete()
    data = await state.get_data()
    question_id = await data.get("question_id")
    msg = await bot.send_message(
        chat_id=chat_id,
        text="Введите ответ на вопрос текстом:",
        reply_markup=question_keyboard(question_id=question_id),
    )
    messages = data.get("message_for_delete", [])
    messages.append(msg.id)
    await state.update_data(message_for_delete=messages)
    await state.set_state(StatesBot.ANSWER_QUESTION)


# Перейти в состоянеи ожидания сообщения
@router.callback_query(ContestantQuestionCallbackFactory.filter(F.action == QuestionState.REJECTED))
async def reject_callback(
    callback: types.CallbackQuery,
    callback_data: ContestantQuestionCallbackFactory,
    db_session: AsyncSession,
    state: FSMContext,
):
    await callback.message.delete()
    await update_state(question_id=callback_data.question_id, state=QuestionState.REJECTED, db_session=db_session)
    await callback.answer("Вопрос отклонён")
    await state.clear()
