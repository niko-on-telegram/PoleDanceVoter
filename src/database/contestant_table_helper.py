import asyncio
from database.database_connector import get_db
from database.crud.contestant import add_contestant_to_db


async def create_contestants(db):
    async with db.session_factory.begin() as db_session:
        await add_contestant_to_db(db_session, db)


def main():
    db = get_db()
    asyncio.run(create_contestants(db))


if __name__ == '__main__':
    main()
