from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callbacks.moderation_factory import ModerationCallbackFactory
from bot.enums import QuestionState
from bot.keyboards.contestant_question_kb import question_keyboard
from database.crud.questions import get_question, update_state

router = Router()


@router.callback_query(ModerationCallbackFactory.filter(F.state == QuestionState.WAITING_RESPONSE))
async def waiting_response_callback(
    callback: types.CallbackQuery,
    callback_data: ModerationCallbackFactory,
    state: FSMContext,
    db_session: AsyncSession,
    bot: Bot,
):
    await callback.message.delete()

    question = await get_question(question_id=callback_data.question_id, db_session=db_session)
    await bot.send_message(
        chat_id=question.competitor_id,
        text=f'Вам пришёл вопрос "{question.question}":',
        reply_markup=question_keyboard(question.id),
    )
    await update_state(
        question_id=callback_data.question_id,
        state=QuestionState.WAITING_RESPONSE,
        db_session=db_session,
    )
    await state.clear()
    await callback.answer("Вопрос согласован")


@router.callback_query(ModerationCallbackFactory.filter(F.state == QuestionState.MODERATION_REJECT))
async def reject_callback(
    callback: types.CallbackQuery,
    callback_data: ModerationCallbackFactory,
    state: FSMContext,
    db_session: AsyncSession,
):
    await callback.message.delete()
    await update_state(
        question_id=callback_data.question_id,
        state=QuestionState.MODERATION_REJECT,
        db_session=db_session,
    )
    await state.clear()
    await callback.answer("Вопрос отклонён")
