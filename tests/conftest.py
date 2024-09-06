import asyncio
import os

import pytest
import pytest_asyncio
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from testcontainers.postgres import PostgresContainer

from bot.callbacks.contestant_factory import ContestantCallbackFactory
from bot.callbacks.votes_factory import VotesCallbackFactory
from bot.enums import ContestantEnum, VotesEnum
from database.database_connector import DatabaseConnector
from database.models import Base, User, Contestant


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
    return User(telegram_id=361557980, full_name="Greed", count_votes=0)


@pytest.fixture
def default_user_username() -> User:
    return User(telegram_id=361557980, username="Uff", full_name="Greed", count_votes=0)


class AIOUser:
    id: int
    full_name: str
    username: str
    count_votes: 0

    def __init__(self, id: int, full_name: str, username: str = "", count_votes: int = 0):
        self.id = id
        self.full_name = full_name
        self.username = username
        self.count_votes = count_votes


@pytest.fixture
def default_user_username_inp() -> AIOUser:
    return AIOUser(id=361557080, full_name="User1", username="Name1", count_votes=0)


@pytest.fixture
def default_user_list_inp() -> list[AIOUser]:
    return [
        AIOUser(id=361557080, full_name="User1", username="Name1", count_votes=0),
        AIOUser(id=361557081, full_name="User2", username="Name2", count_votes=3),
        AIOUser(id=361557082, full_name="User3", username="Name3", count_votes=0),
        AIOUser(id=361557083, full_name="User4", username="Name4", count_votes=0),
        AIOUser(id=361557084, full_name="User5", username="Name5", count_votes=0),
    ]


@pytest.fixture
def default_user_list() -> list[User]:
    return [
        User(telegram_id=361557080, full_name="User1", count_votes=0),
        User(telegram_id=361557081, full_name="User2", count_votes=3),
        User(telegram_id=361557082, full_name="User3", count_votes=0),
        User(telegram_id=361557083, full_name="User4", count_votes=0),
        User(telegram_id=361557084, full_name="User5", count_votes=0),
    ]


@pytest.fixture
def default_user_list_username() -> list[User]:
    return [
        User(telegram_id=361557080, full_name="User1", username="UserName1", count_votes=0),
        User(telegram_id=361557081, full_name="User2", username="UserName1", count_votes=3),
        User(telegram_id=361557082, full_name="User3", username="UserName1", count_votes=0),
        User(telegram_id=361557083, full_name="User4", username="UserName1", count_votes=0),
        User(telegram_id=361557084, full_name="User5", username="UserName1", count_votes=0),
    ]


@pytest.fixture
def default_contestants_list(default_user) -> list[Contestant]:
    return [
        Contestant(
            telegram_id=361557982,
            full_name="Contestnat1",
            count_votes=0,
            description="description1",
            video_first="video1",
            video_second="video2",
            video_third="video3",
        ),
        Contestant(
            telegram_id=361557984,
            full_name="Contestnat2",
            count_votes=1,
            description="description2",
            video_first="video1",
            video_second="video2",
            video_third="video3",
        ),
        Contestant(
            telegram_id=361557985,
            full_name="Contestnat3",
            count_votes=2,
            description="description3",
            video_first="video1",
            video_second="video2",
            video_third="video3",
        ),
        Contestant(
            telegram_id=361557986,
            full_name="Contestnat4",
            count_votes=3,
            description="description4",
            video_first="video1",
            video_second="video2",
            video_third="video3",
        ),
        Contestant(
            telegram_id=361557987,
            full_name="Contestnat5",
            count_votes=4,
            description="description5",
            video_first="video1",
            video_second="video2",
            video_third="video3",
        ),
    ]


@pytest.fixture
def default_contestant_keyboard(default_user, default_contestants_list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Проголосовать',
        callback_data=ContestantCallbackFactory(
            user_id=default_user.telegram_id,
            contestant_id=default_contestants_list[0].telegram_id,
            action=ContestantEnum.VOTE,
        ),
    )
    kb.button(
        text='Задать вопрос',
        callback_data=ContestantCallbackFactory(
            user_id=default_user.telegram_id,
            contestant_id=default_contestants_list[0].telegram_id,
            action=ContestantEnum.QUESTION,
        ),
    )
    kb.button(
        text='Посмотреть ответы',
        callback_data=ContestantCallbackFactory(
            user_id=default_user.telegram_id,
            contestant_id=default_contestants_list[0].telegram_id,
            action=ContestantEnum.CHECK_ANSWER,
        ),
    )
    kb.button(
        text='К списку участников',
        callback_data=ContestantCallbackFactory(
            user_id=default_user.telegram_id,
            contestant_id=default_contestants_list[0].telegram_id,
            action=ContestantEnum.BACK,
        ),
    )
    kb.adjust(1)
    return kb.as_markup()


@pytest.fixture
def default_contestants_kb(default_user: User, default_contestants_list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for num in range(len(default_contestants_list)):
        kb.button(
            text=f'{default_contestants_list[num].full_name}     Голоса: {default_contestants_list[num].count_votes}',
            callback_data=ContestantCallbackFactory(
                contestant_id=default_contestants_list[num].telegram_id,
                user_id=default_user.telegram_id,
                action=ContestantEnum.PROFILE,
            ),
        )
    kb.adjust(1)
    return kb.as_markup()


@pytest.fixture
def default_vote_kb(default_user: User, default_contestants_list: list[Contestant]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Проголосовать",
        callback_data=VotesCallbackFactory(
            user_id=default_user.telegram_id,
            contestant_id=default_contestants_list[0].telegram_id,
            action=VotesEnum.VOTE,
        ),
    )
    kb.button(
        text="Назад",
        callback_data=VotesCallbackFactory(
            user_id=default_user.telegram_id,
            contestant_id=default_contestants_list[0].telegram_id,
            action=VotesEnum.BACK,
        ),
    )
    kb.adjust(1)
    return kb.as_markup()


@pytest.fixture
def default_contestant_callback_factory_back(default_user, default_contestants_list) -> ContestantCallbackFactory:
    return ContestantCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=ContestantEnum.BACK,
    )


@pytest.fixture
def default_contestant_callback_factory_vote(default_user, default_contestants_list) -> ContestantCallbackFactory:
    return ContestantCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=ContestantEnum.VOTE,
    )


@pytest.fixture
def default_contestant_callback_factory_question(default_user, default_contestants_list) -> ContestantCallbackFactory:
    return ContestantCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=ContestantEnum.QUESTION,
    )


@pytest.fixture
def default_contestant_callback_factory_check_answer(
    default_user, default_contestants_list
) -> ContestantCallbackFactory:
    return ContestantCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=ContestantEnum.CHECK_ANSWER,
    )


@pytest.fixture
def default_contestant_callback_factory_profile(default_user, default_contestants_list) -> ContestantCallbackFactory:
    return ContestantCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=ContestantEnum.PROFILE,
    )


@pytest.fixture
def default_votes_callback_factory_back(default_user, default_contestants_list) -> VotesCallbackFactory:
    return VotesCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=VotesEnum.BACK,
    )


@pytest.fixture
def default_votes_callback_factory_vote(default_user, default_contestants_list) -> VotesCallbackFactory:
    return VotesCallbackFactory(
        user_id=default_user.telegram_id,
        contestant_id=default_contestants_list[0].telegram_id,
        action=VotesEnum.VOTE,
    )
