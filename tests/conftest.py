import asyncio
import os

import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer

from database.database_connector import DatabaseConnector
from database.models import Base, User


@pytest_asyncio.fixture()
async def db(pytestconfig):
    postgres = PostgresContainer("postgres:15", driver="asyncpg")
    postgres.start()

    test_database = DatabaseConnector(url=postgres.get_connection_url(), echo=True)
    async with test_database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    yield test_database

    await test_database.engine.dispose()
    postgres.stop()


@pytest.fixture
def default_user() -> User:
    return User(telegram_id=361557982, fullname="Greed", count_votes=0)
