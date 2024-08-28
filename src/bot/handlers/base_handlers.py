from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import URLInputFile

from database.models import User

from bot.keyboards.contestant_list import get_contestant_list
from database.crud.contestant import get_all_contestants

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, user: User, db_session) -> None:
    contestants = await get_all_contestants(db_session)
    await message.answer_photo(
        URLInputFile(
            "https://cdn1.flamp.ru/1489ba9b728d7498f6856aa144123716.jpeg",
            filename="1489ba9b728d7498f6856aa144123716.jpeg",
        ),
        caption=f'Hello, {user.fullname}. Список участников:',
        reply_markup=get_contestant_list(contestants),
    )
