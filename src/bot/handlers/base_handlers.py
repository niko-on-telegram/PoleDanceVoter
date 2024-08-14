from aiogram import Router, types
from aiogram.filters import CommandStart

from database.models import User

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, user: User) -> None:
    await message.answer(text=f'Hello, {user.fullname}.')
