from aiogram import Router, F, types, Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.moderation_factory import ModerationCallbackFactory
from bot.enums import QuestionState
from bot.keyboards.contestant_question_kb import question_keyboard
from database.crud.questions import update_state, get_question

router = Router()


@router.callback_query(ModerationCallbackFactory.filter(F.action == QuestionState.WAITING_RESPONSE))
async def waiting_response_callback(
    callback: types.CallbackQuery, callback_data: ModerationCallbackFactory, db_session: AsyncSession, bot: Bot
):
    await callback.message.delete()

    question = await get_question(question_id=callback_data.question_id, db_session=db_session)
    await bot.send_message(
        chat_id=question.contestant_id, text=question.question, reply_markup=question_keyboard(question.id)
    )
    await update_state(
        question_id=callback_data.question_id, state=QuestionState.WAITING_RESPONSE, db_session=db_session
    )
    await callback.answer("Вопрос согласован")


@router.callback_query(ModerationCallbackFactory.filter(F.action == QuestionState.MODERATION_REJECT))
async def reject_callback(
    callback: types.CallbackQuery, callback_data: ModerationCallbackFactory, db_session: AsyncSession
):
    await callback.message.delete()
    await update_state(
        question_id=callback_data.question_id, state=QuestionState.MODERATION_REJECT, db_session=db_session
    )
    await callback.answer("Вопрос отклонён")
