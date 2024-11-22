import logging
import traceback
import typing

import aiogram
from aiogram import Router, html

from config import settings

if typing.TYPE_CHECKING:
    from aiogram.types.error_event import ErrorEvent

router = Router()


@router.errors()
async def error_handler(error_event: "ErrorEvent", bot: aiogram.Bot):
    exc_info = error_event.exception
    exc_traceback = "".join(traceback.format_exception(None, exc_info, exc_info.__traceback__))

    tb = html.quote(exc_traceback[-3500:])
    exc_name = html.quote(type(exc_info).__name__)
    exc_info = html.quote(str(exc_info))

    error_message = (
        f"🚨 <b>An error occurred</b> 🚨\n\n"
        f"<b>Type:</b> {exc_name}\n<b>Message:</b> {exc_info}\n\n<b>Traceback:</b>\n<code>{tb}</code>"
    )
    logging.exception("Exception:", exc_info=exc_info)

    await bot.send_message(settings.ADMIN, error_message)
