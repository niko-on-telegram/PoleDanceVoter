from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Voter


async def get_all_voter_ids(user_id: int, db_session: AsyncSession) -> list[Voter]:
    query = select(Voter)
    result = await db_session.execute(query)
    return list(result.scalars().all())


async def add_voter_to_db(user_id: int, contestant_id: int, db_session: AsyncSession):
    voters = await get_all_voter_ids(user_id, db_session)
    for voter in voters:
        if voter.contestant_id == contestant_id:
            break
    else:
        voter = Voter(user_id=user_id, contestant_id=contestant_id, vote_state="vote")
        db_session.add(voter)
