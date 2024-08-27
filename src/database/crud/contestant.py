from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Contestant


async def get_contestant_from_db(tg_id: int, db_session) -> Contestant:
    query = select(Contestant).filter(Contestant.telegram_id == tg_id)
    result: Result = await db_session.execute(query)
    contestant = result.scalar()
    return contestant


async def get_all_contestants(db_session: AsyncSession) -> list[Contestant]:
    query = select(Contestant)
    result = await db_session.execute(query)
    return list(result.scalars().all())
