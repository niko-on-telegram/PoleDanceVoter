from aiogram import Router, types
from aiogram.filters import CommandStart

from database.models import User

from bot.internal.hello_img import hello_img
from bot.keyboards.contestant_list import get_contestant_list
from database.crud.contestant import get_all_contestants

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, user: User, db_session) -> None:
    contestants = await get_all_contestants(db_session)
    await message.answer_photo(
        hello_img,
        caption=f'Hello, {user.fullname}. Список участников:',
        reply_markup=get_contestant_list(contestants),
    )
