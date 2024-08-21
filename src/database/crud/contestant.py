from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Contenstant


async def add_contestant_to_db(db_session):
    contestants = [Contenstant(telegram_id=361557983, fullname="Снежанна", count_votes=13),
                   Contenstant(telegram_id=361557984, fullname="Владислав", count_votes=455),
                   Contenstant(telegram_id=361557985, fullname="Педро", count_votes=666),
                   Contenstant(telegram_id=361557986, fullname="Анжелика", count_votes=234),
                   Contenstant(telegram_id=361557987, fullname="Гоги", count_votes=137),
                   Contenstant(telegram_id=361557988, fullname="Рикардо", count_votes=999),
                   Contenstant(telegram_id=361557989, fullname="Белатриса", count_votes=453),
                   Contenstant(telegram_id=361557990, fullname="Кирилл", count_votes=15),
                   Contenstant(telegram_id=361557991, fullname="Анна", count_votes=18),
                   Contenstant(telegram_id=361557992, fullname="Зульфия", count_votes=19)]

    for contestant in contestants:
        db_session.add(contestant)


async def get_all_contestants(db_session: AsyncSession) -> list[Contenstant]:
    query = select(Contenstant)
    result = await db_session.execute(query)
    return list(result.scalars().all())
