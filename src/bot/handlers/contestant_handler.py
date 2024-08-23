from aiogram import Router, types
from aiogram import F
from bot.keyboards.contestant_choose import get_contestant

router = Router()


@router.callback_query(F.data == "Contestant")
async def send_contestant_choose(callback: types.CallbackQuery):
    await callback.message.answer(text="Answer", reply_markup=get_contestant())
