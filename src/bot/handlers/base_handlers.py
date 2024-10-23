from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.helpers import print_constestant_list

router = Router()


@router.message(CommandStart())
async def start_message(message: types.Message, db_session, state: FSMContext) -> None:
    await state.set_state()
    await print_constestant_list(message, db_session)
