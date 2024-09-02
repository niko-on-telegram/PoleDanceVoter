import asyncio
import os

import pytest
import pytest_asyncio
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from testcontainers.postgres import PostgresContainer

from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.enums import ContestantEnum
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
def empty_tg_id() -> int:
    return 361557981


@pytest.fixture
def default_user() -> User:
    return User(telegram_id=361557982, fullname="Greed", count_votes=0)


@pytest.fixture
def default_user_username() -> User:
    return User(telegram_id=361557982, username="Uff", fullname="Greed", count_votes=0)


@pytest.fixture
def default_user_list(default_user) -> list[User]:
    return [
        default_user,
        User(telegram_id=361557984, fullname="User2", count_votes=1),
        User(telegram_id=361557985, fullname="User3", count_votes=2),
        User(telegram_id=361557986, fullname="User4", count_votes=3),
        User(telegram_id=361557987, fullname="User5", count_votes=4),
    ]


@pytest.fixture
def default_user_list_username(default_user_username) -> list[User]:
    return [
        default_user_username,
        User(telegram_id=361557984, fullname="User2", count_votes=1),
        User(telegram_id=361557985, fullname="User3", count_votes=2),
        User(telegram_id=361557986, fullname="User4", count_votes=3),
        User(telegram_id=361557987, fullname="User5", count_votes=4),
    ]


@pytest.fixture
def contestants_kb(default_user: User, default_user_list: list[User]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for num in range(len(default_user_list)):
        kb.button(
            text=f'{default_user_list[num].fullname}     Голоса: {default_user_list[num].count_votes}',
            callback_data=ContestantCallbackFactory(
                contestant_id=default_user_list[num].telegram_id,
                user_id=default_user.telegram_id,
                action=ContestantEnum.PROFILE,
            ),
        )
    kb.adjust(1)
    return kb.as_markup()
