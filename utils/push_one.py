import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from videoprops import get_video_properties

from bot.internal.hello_img import logo_label
from config import settings
from database.database_connector import get_db
from database.models import Competitor, Resource


session = AiohttpSession(timeout=1200, api=TelegramAPIServer.from_base('http://localhost:8081'))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: " "%(filename)s: " "%(levelname)s: " "%(funcName)s(): " "%(lineno)d:\t" "%(message)s",
)


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
    pp = "/home/gridgain/PycharmProjects/PoleDanceVoter/data/competitors_data_compreseed_optimized/competitors_data/Tatyana Denisenkova/presentation2.mp4"
    tumb = "/home/gridgain/PycharmProjects/PoleDanceVoter/data/competitors_data_compreseed_optimized/competitors_data/Tatyana Denisenkova/empty.jpg"
    assert Path(pp).exists()
    props = get_video_properties(pp)
    print(props)
    msg = await bot.send_video(99988303, video=FSInputFile(pp), width=props['width'], height=props['height'],
                               thumbnail=FSInputFile(tumb),
                               supports_streaming=True)
    print(f"{msg.video.file_id=}")
    await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
