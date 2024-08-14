from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def add_user_to_db(user, db_session) -> User:
    new_user = User(
        telegram_id=user.id,
        fullname=user.full_name,
        username=user.username,
    )
    db_session.add(new_user)
    await db_session.flush()
    return new_user


async def get_user_from_db_by_tg_id(telegram_id: int, db_session: AsyncSession) -> User | None:
    query = select(User).filter(User.telegram_id == telegram_id)
    result: Result = await db_session.execute(query)
    user = result.scalar()
    return user


async def get_all_users_ids(db_session: AsyncSession) -> list[User.telegram_id]:
    query = select(User.telegram_id)
    result = await db_session.execute(query)
    return list(result.scalars().all())
