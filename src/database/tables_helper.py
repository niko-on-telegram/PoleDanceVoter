import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine

from database.database_connector import get_db
from database.models import Base


async def create_or_drop_db(engine: AsyncEngine, create: bool = True):
    async with engine.begin() as conn:
        if create:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        else:
            await conn.run_sync(Base.metadata.drop_all)


def main():
    db = get_db()
    asyncio.run(create_or_drop_db(db.engine))


if __name__ == '__main__':
    main()
