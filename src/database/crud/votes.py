import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Votes


async def get_all_votes_ids(telegram_user_id: int, db_session: AsyncSession) -> list[Votes]:
    query = select(Votes).filter(Votes.user_id == telegram_user_id)
    result = await db_session.execute(query)
    return list(result.scalars().all())


async def add_votes_to_db(user_id: int, competitor_id: int, db_session: AsyncSession):
    votes = await get_all_votes_ids(user_id, db_session)
    for vote in votes:
        if vote.competitor_id == competitor_id:
            logging.warning(f"Last check save for {competitor_id}")
            break
    else:
        votes = Votes(user_id=user_id, competitor_id=competitor_id, vote_state="vote")
        db_session.add(votes)
