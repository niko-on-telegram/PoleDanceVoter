from aiogram import Router, types
from aiogram import F
from bot.keyboards.contestant_choose import get_contestant
from aiogram.types import InputMediaVideo

router = Router()


@router.callback_query(F.data == "Contestant")
async def send_contestant_choose(callback: types.CallbackQuery):
    await callback.message.answer_media_group(
        protect_content=True,
        media=[
            InputMediaVideo(media='BAACAgIAAxkDAAIBMGbJmZYh8HYpGld5Pgybhf_QRPHzAAKHTwAC_WFQSqQ9YspmOnw1NQQ'),
            InputMediaVideo(media='BAACAgIAAxkDAAIBMWbJmZjC9wVPzsCEAAFmDmTRbS9wfAACiE8AAv1hUEojFGA6JfOJKjUE'),
            InputMediaVideo(media='BAACAgIAAxkDAAIBMmbJmZrOtqpuFu10J8bvmNV9XRysAAKJTwAC_WFQSvh55_QXgQM4NQQ'),
        ],
        reply_markup=get_contestant(),
    )
    await callback.message.answer(text='Здесь могло быть ваше описание', reply_markup=get_contestant())
