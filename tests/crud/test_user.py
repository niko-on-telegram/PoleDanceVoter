import pytest
from sqlalchemy import select, Result

from database.models import User
from database.crud.user import inc_dec_vote_to_db, get_user_from_db_by_tg_id, get_all_users_ids, add_user_to_db
from tests.default_entity_db.user import (
    get_default_user,
    get_default_user_username,
    get_defult_user_list,
    get_defult_user_list_username,
    empty_tg_id,
)


# get_user_from_db_by_tg_id
@pytest.mark.asyncio
async def test_check_get_user_from_db_by_tg_id_none(db):
    default_user = get_default_user()
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user, db_session)

    async with db.session_factory() as db_session:
        user = await get_user_from_db_by_tg_id(empty_tg_id, db_session)
        assert user is None


@pytest.mark.asyncio
async def test_check_get_user_from_db_by_tg_id_usrname(db):
    default_user = get_default_user_username()
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user, db_session)

    async with db.session_factory() as db_session:
        user = await get_user_from_db_by_tg_id(default_user.telegram_id, db_session)
        assert default_user == user


@pytest.mark.asyncio
async def test_check_get_user_from_db_by_tg_id(db):
    default_user = get_default_user()
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user, db_session)

    async with db.session_factory() as db_session:
        user = await get_user_from_db_by_tg_id(default_user.telegram_id, db_session)
        assert default_user == user


# add_user_to_db
@pytest.mark.asyncio
async def test_check_one_user_add_to_db_func(db):
    default_user = get_default_user()
    async with db.session_factory.begin() as db_session:
        test_user = await add_user_to_db(default_user, db_session)
        assert default_user == test_user


@pytest.mark.asyncio
async def test_check_one_user_add_to_db(db):
    default_user = get_default_user()
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user, db_session)
        query = select(User).filter(User.telegram_id == default_user.telegram_id)
        result: Result = await db_session.execute(query)
        db_user = result.scalar()
        assert default_user == db_user


@pytest.mark.asyncio
async def test_check_one_user_add_to_db_func_usrname(db):
    default_user = get_default_user_username()
    async with db.session_factory.begin() as db_session:
        test_user = await add_user_to_db(default_user, db_session)
        assert default_user == test_user


@pytest.mark.asyncio
async def test_check_one_user_add_to_db_usrname(db):
    default_user = get_default_user_username()
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user, db_session)
        query = select(User).filter(User.telegram_id == default_user.telegram_id)
        result: Result = await db_session.execute(query)
        db_user = result.scalar()
        assert default_user == db_user
