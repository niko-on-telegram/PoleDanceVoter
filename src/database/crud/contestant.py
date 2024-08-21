from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Contenstant


async def add_contestant_to_db(contestant: Contenstant, db_session) -> Contenstant:
    new_contestant = Contenstant(
        telegram_id=contestant.telegram_id,
        fullname=contestant.fullname,
        description=contestant.description,
        count_votes=contestant.count_votes,
        video_first=contestant.video_first,
        video_second=contestant.video_second,
        video_third=contestant.video_third
    )
    db_session.add(new_contestant)
    await db_session.flush()
    return new_contestant


async def get_contestant_from_db_by_tg_id(telegram_id: int, db_session: AsyncSession) -> Contenstant | None:
    query = select(Contenstant).filter(Contenstant.telegram_id == telegram_id)
    result: Result = await db_session.execute(query)
    user = result.scalar()
    return user


async def get_all_users_ids(db_session: AsyncSession) -> list[Contenstant.telegram_id]:
    query = select(Contenstant.telegram_id)
    result = await db_session.execute(query)
    return list(result.scalars().all())
