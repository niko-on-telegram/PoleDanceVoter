from email import message_from_file

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import QuestionState
from database.crud.questions import add_question_to_db

router = Router()


@router.message(F.text)
async def get_message(message: Message, db_session: AsyncSession):

    contestant_id = 1
    await add_question_to_db(contestant_id, message.from_user.id, message.text, QuestionState.MODERATION, db_session)

    await message.answer("Спасибо за вопрос!")
    #await print_profile(contestant_id, message.message_id, db_session)


# async def print_profile(contestant_id: int, last_message: int, db_session: AsyncSession):
#     await callback.message.delete()
#     await callback.bot.delete_message(chat_id=callback_data.chat_id, message_id=callback_data.video1_id)
#     await callback.bot.delete_message(chat_id=callback_data.chat_id, message_id=callback_data.video2_id)
#     await callback.bot.delete_message(chat_id=callback_data.chat_id, message_id=callback_data.video3_id)
#
#     contestant = await get_contestant_from_db(contestant_id, db_session)
#     message_list = await callback.message.answer_media_group(
#         protect_content=True,
#         media=[
#             InputMediaVideo(media=contestant.video_first),
#             InputMediaVideo(media=contestant.video_second),
#             InputMediaVideo(media=contestant.video_third),
#         ],
#     )
#     await callback.message.answer(
#         text=contestant.description,
#         reply_markup=contestant_keyboard(
#             user_id=callback_data.user_id,
#             contestant_id=callback_data.contestant_id,
#             video1_id=message_list[0].message_id,
#             video2_id=message_list[1].message_id,
#             video3_id=message_list[2].message_id,
#             chat_id=message_list[0].chat.id,
#         ),
#     )
#     await callback.answer()


@router.message()
async def get_any_message(message: Message, state: FSMContext):
    msg = await message.answer("Вы ввели не текст! Введите только текст.")
    data = await state.get_data()
    messages = data.get("message_for_delete", [])
    messages.append(msg.id)
    messages.append(message.id)
    await state.update_data(message_for_delete=messages)
    return