from aiogram import Router, F, types, Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.contestant_question_factory import ContestantQuestionCallbackFactory
from bot.enums import QuestionState
from database.crud.questions import update_state, get_question

router = Router()


@router.callback_query(ContestantQuestionCallbackFactory.filter(F.action == QuestionState.WAITING_RESPONSE))
async def waiting_response_callback(
    callback: types.CallbackQuery, bot: Bot):
    chat_id = callback.message.chat_id
    await callback.message.delete()

    await bot.send_message(chat_id=chat_id, text="Введите ответ на вопрос текстом:")

   # Получить ответ на вопрос или выдать клавиатуру номер 2 для ответа пустого или не текстаа



@router.callback_query(ContestantQuestionCallbackFactory.filter(F.action == QuestionState.REJECTED))
async def reject_callback(
    callback: types.CallbackQuery, callback_data: ContestantQuestionCallbackFactory, db_session: AsyncSession
):
    await callback.message.delete()
    await update_state(question_id=callback_data.question_id, state=QuestionState.REJECTED, db_session=db_session)
    await callback.answer("Вопрос отклонён")
