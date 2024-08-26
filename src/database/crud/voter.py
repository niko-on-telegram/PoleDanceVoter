from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Voter


async def get_user_from_db_by_tg_id(user_id: int, db_session: AsyncSession) -> Voter | None:
    query = select(Voter).filter(Voter.user_id == user_id)
    result: Result = await db_session.execute(query)
    voter = result.scalar()
    return voter
