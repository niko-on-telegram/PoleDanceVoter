import logging

from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.helpers import print_constestant_list

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, db_session, state: FSMContext) -> None:
    await state.set_state()
    await print_constestant_list(message, db_session)


@router.message(F.video)
async def video_message(message: types.Message, bot: Bot) -> None:
    if message.from_user.id not in [99988303, 309535280]:
        logging.info("Unexpexted video sent")
        return
    fmtted = f"{message.video.file_name=} {message.video.file_id=}"
    await bot.send_message(99988303, fmtted)
    await message.answer(fmtted)
