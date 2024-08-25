from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from aiogram.client.default import DefaultBotProperties
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
import os
from config import settings
from database.models import Contestant

bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def get_contestant_from_db(tg_id: int, db_session) -> Contestant:
    query = select(Contestant).filter(Contestant.telegram_id == tg_id)
    result: Result = await db_session.execute(query)
    contestant = result.scalar()
    return contestant


async def get_file_id() -> list[str]:
    files = []

    path_to_videos = '/home/greed/work/'
    for i in 1, 2, 3:
        img_path = os.path.join(path_to_videos, '111.mp4')
        message = await bot.send_video(settings.ADMIN, FSInputFile(img_path))
        print(f"Iter {i} path {img_path} id {message.video.file_id}")
        files.append(message.video.file_id)
    return files


async def add_contestant_to_db(db_session):
    contestants = []
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557983,
            fullname="Снежанна",
            count_votes=13,
            description="Текст 1",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557984,
            fullname="Владислав",
            count_votes=143,
            description="Текст 2",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557985,
            fullname="Педро",
            count_votes=1563,
            description="Текст 3",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557986,
            fullname="Анжелика",
            count_votes=1653,
            description="Текст 4",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557987,
            fullname="Гоги",
            count_votes=16543,
            description="Текст 5",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557988,
            fullname="Рикардо",
            count_votes=1342,
            description="Текст 6",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557989,
            fullname="Белатриса",
            count_votes=173,
            description="Текст 7",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557990,
            fullname="Кирилл",
            count_votes=183,
            description="Текст 8",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557991,
            fullname="Анна",
            count_votes=1334,
            description="Текст 9",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )
    videos = await get_file_id()
    contestants.append(
        Contestant(
            telegram_id=361557992,
            fullname="Зульфия",
            count_votes=1334,
            description="Текст 10",
            video_first=videos[0],
            video_second=videos[1],
            video_third=videos[2],
        )
    )

    for contestant in contestants:
        db_session.add(contestant)


async def get_all_contestants(db_session: AsyncSession) -> list[Contestant]:
    query = select(Contestant)
    result = await db_session.execute(query)
    return list(result.scalars().all())
