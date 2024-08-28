import logging
import os
import pytest_asyncio
from testcontainers.postgres import PostgresContainer

from database.database_connector import DatabaseConnector


@pytest_asyncio.fixture()
async def db(pytestconfig):
    pole_dance_voter_dir = os.path.join(pytestconfig.rootpath, "pole_dance_voter")
    postgres = PostgresContainer("postgres:15", driver="asyncpg")
    postgres.start()

    test_database = DatabaseConnector(url=postgres.get_connection_url(), echo=True)
    async with test_database.engine.begin() as db_session:
        #TODO: run main tests

    yield test_database

    await test_database.engine.dispose()
    postgres.stop()
