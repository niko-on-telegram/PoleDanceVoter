import logging

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.helpers import print_constestant_list

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, db_session, state: FSMContext) -> None:
    await state.set_state()
    await print_constestant_list(message, db_session)


@router.message(F.video)
async def video_message(message: types.Message) -> None:
    if message.from_user.id != 99988303:
        logging.info("Unexpexted video sent")
        return

    await message.answer(f"{message.video.file_name=} {message.video.file_id=}")
