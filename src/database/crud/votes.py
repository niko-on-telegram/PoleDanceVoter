from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Votes


async def get_all_votes_ids(user_id: int, db_session: AsyncSession) -> list[Votes]:
    query = select(Votes)
    result = await db_session.execute(query)
    return list(result.scalars().all())


async def add_votes_to_db(user_id: int, contestant_id: int, db_session: AsyncSession):
    votes = await get_all_votes_ids(user_id, db_session)
    for vote in votes:
        if vote.contestant_id == contestant_id:
            break
    else:
        votes = Votes(user_id=user_id, contestant_id=contestant_id, vote_state="vote")
        db_session.add(votes)
