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

session = AiohttpSession(timeout=1200, api=TelegramAPIServer.from_base("http://localhost:8081"))
bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session,
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: " "%(filename)s: " "%(levelname)s: " "%(funcName)s(): " "%(lineno)d:\t" "%(message)s",
)


async def process_media(file_path) -> str:
    file = FSInputFile(file_path)
    logging.info(f"Processing media: {file_path.name}, size: {file_path.stat().st_size / 1000000} MB")
    match file_path.suffix.lower():
        case ".png" | ".jpg":
            msg = await bot.send_photo(chat_id=settings.ADMIN, photo=file)
            media_id = msg.photo[-1].file_id
        case ".mp4":
            # get width and height
            props = get_video_properties(file_path)
            msg = await bot.send_video(
                chat_id=settings.ADMIN,
                video=file,
                width=props["width"],
                height=props["height"],
                supports_streaming=True,
            )
            media_id = msg.video.file_id
        case _:
            assert False, f"Unexpected file type: {file_path.suffix}"

    return media_id


async def folder_walker():
    main_folder = Path("./data/competitors_data")
    assert main_folder.exists(), f"Folder {main_folder.absolute()} not found"
    competitors = os.listdir(main_folder)
    logging.info(f"{competitors=}")

    for competitor in competitors:
        logging.info(f"{competitor=}")
        new_competitor = dict()
        new_competitor["photos"] = []
        for subdir, dirs, files in os.walk(main_folder / competitor):
            for file in files:
                match file.lower():
                    case "tg_id.txt":
                        logging.info(f"Processing tg_id...")
                        with open(os.path.join(subdir, file)) as f:
                            tg_id = int(f.read())
                        new_competitor["telegram_id"] = tg_id
                    case i if i.startswith("photo"):
                        file_path = Path(subdir) / file
                        media_id = await process_media(file_path)
                        new_competitor["photos"].append(media_id)
                    case "video_cut.mp4":
                        file_path = Path(subdir) / file
                        media_id = await process_media(file_path)
                        new_competitor["dance_cut"] = media_id
                    case "video_uncut.mp4":
                        file_path = Path(subdir) / file
                        media_id = await process_media(file_path)
                        new_competitor["dance_uncut"] = media_id
                    case i if i.startswith("afisha"):
                        file_path = Path(subdir) / file
                        media_id = await process_media(file_path)
                        new_competitor["poster"] = media_id
                    case i if i.startswith("presentation"):
                        file_path = Path(subdir) / file
                        media_id = await process_media(file_path)
                        new_competitor["presentation"] = media_id
                    case "info.txt":
                        logging.info(f"Processing info...")
                        with open(os.path.join(subdir, file)) as f:
                            lines = f.readlines()
                        full_name = lines[0].strip()
                        info = "".join(lines[1:]).strip()
                        new_competitor["full_name"] = full_name
                        new_competitor["info"] = info
                    case _:
                        raise RuntimeError(f"Unexpected file {competitor=} {file=}")
        new_competitor["photos"] = ", ".join(new_competitor["photos"])
        db = get_db(settings)
        async with db.session_factory.begin() as db_session:
            db_session.add(Competitor(**new_competitor))
    await bot.session.close()


async def resources_populate():
    main_logo = Path("./data/logo.jpg")
    assert main_logo.exists(), f"Folder {main_logo.absolute()} not found"
    db = get_db(settings)
    logo_id = await process_media(main_logo)
    async with db.session_factory.begin() as db_session:
        db_session.add(Resource(label=logo_label, file_id=logo_id))

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(resources_populate())
    asyncio.run(folder_walker())
