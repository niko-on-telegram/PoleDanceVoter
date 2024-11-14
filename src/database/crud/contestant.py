from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Competitor, Resource


async def inc_dec_vote_to_db(tg_id: int, db_session: AsyncSession, inc: bool = True):
    query = select(Competitor).filter(Competitor.telegram_id == tg_id)
    result: Result = await db_session.execute(query)
    contestant = result.scalar()
    votes = contestant.count_votes + 1 if inc else contestant.count_votes - 1
    updates = update(Competitor).where(Competitor.telegram_id == tg_id).values(count_votes=votes)
    await db_session.execute(updates)


async def get_competitor_from_db(tg_id: int, db_session) -> Competitor:
    query = select(Competitor).filter(Competitor.telegram_id == tg_id)
    result: Result = await db_session.execute(query)
    contestant = result.scalar()
    return contestant


async def get_all_contestants(db_session: AsyncSession) -> list[Competitor]:
    query = select(Competitor).order_by(Competitor.id)
    result = await db_session.execute(query)
    return list(result.scalars().all())


async def get_resource(resource_label: str, db_session: AsyncSession) -> str:
    query = select(Resource.file_id).where(Resource.label == resource_label)
    result = await db_session.execute(query)
    return result.scalar_one()
