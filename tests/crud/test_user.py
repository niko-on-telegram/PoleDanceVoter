import pytest
from sqlalchemy import select, Result

from database.models import User
from database.crud.user import inc_dec_vote_to_db, get_user_from_db_by_tg_id, get_all_users_ids, add_user_to_db


# inc_dec_vote_to_db
@pytest.mark.asyncio
async def test_inc_vot_to_db(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory.begin() as db_session:
        await inc_dec_vote_to_db(default_user_username_inp.id, db_session)

    async with db.session_factory.begin() as db_session:
        user = await get_user_from_db_by_tg_id(default_user_username_inp.id, db_session)

    assert user.count_votes == default_user_username_inp.count_votes + 1


@pytest.mark.asyncio
async def test_inc_vot_to_db(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory.begin() as db_session:
        await inc_dec_vote_to_db(default_user_username_inp.id, db_session)

    async with db.session_factory.begin() as db_session:
        user = await get_user_from_db_by_tg_id(default_user_username_inp.id, db_session)

    assert user.count_votes == default_user_username_inp.count_votes + 1


@pytest.mark.asyncio
async def test_dec_vot_to_db(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory.begin() as db_session:
        await inc_dec_vote_to_db(default_user_username_inp.id, db_session, False)

    async with db.session_factory.begin() as db_session:
        user = await get_user_from_db_by_tg_id(default_user_username_inp.id, db_session)

    assert user.count_votes == default_user_username_inp.count_votes - 1


@pytest.mark.asyncio
async def test_dec_vot_to_db(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory.begin() as db_session:
        await inc_dec_vote_to_db(default_user_username_inp.id, db_session, False)

    async with db.session_factory.begin() as db_session:
        user = await get_user_from_db_by_tg_id(default_user_username_inp.id, db_session)

    assert user.count_votes == default_user_username_inp.count_votes - 1


# get_all_users_ids
@pytest.mark.asyncio
async def test_get_all_users_ids_list_username(db, default_user_list_inp):
    async with db.session_factory.begin() as db_session:
        for user in default_user_list_inp:
            await add_user_to_db(user, db_session)

    async with db.session_factory() as db_session:
        users = await get_all_users_ids(db_session)
        assert len(users) == len(default_user_list_inp)
        for user_list, db_user in zip(default_user_list_inp, users):
            assert user_list.id == db_user


@pytest.mark.asyncio
async def test_get_all_users_ids_list(db, default_user_list_inp):
    async with db.session_factory.begin() as db_session:
        for user in default_user_list_inp:
            await add_user_to_db(user, db_session)

    async with db.session_factory() as db_session:
        users = await get_all_users_ids(db_session)
        assert len(users) == len(default_user_list_inp)
        for user_list, db_user in zip(default_user_list_inp, users):
            assert user_list.id == db_user


@pytest.mark.asyncio
async def test_get_all_users_ids_none(db, default_user_username_inp):
    async with db.session_factory() as db_session:
        users = await get_all_users_ids(db_session)
        assert len(users) == 0


@pytest.mark.asyncio
async def test_get_all_users_ids(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory() as db_session:
        users = await get_all_users_ids(db_session)
        assert len(users) == 1
        assert users[0] == default_user_username_inp.id


@pytest.mark.asyncio
async def test_get_all_users_ids_username(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory() as db_session:
        users = await get_all_users_ids(db_session)
        assert len(users) == 1
        assert users[0] == default_user_username_inp.id


# get_user_from_db_by_tg_id
@pytest.mark.asyncio
async def test_check_get_user_from_db_by_tg_id_none(db, default_user_username_inp, empty_tg_id):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory() as db_session:
        user = await get_user_from_db_by_tg_id(empty_tg_id, db_session)
        assert user is None


@pytest.mark.asyncio
async def test_check_get_user_from_db_by_tg_id_usrname(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory() as db_session:
        user = await get_user_from_db_by_tg_id(default_user_username_inp.id, db_session)
        assert default_user_username_inp.id == user.telegram_id
        assert default_user_username_inp.username == user.username
        assert default_user_username_inp.full_name == user.full_name
        assert default_user_username_inp.count_votes == user.count_votes


@pytest.mark.asyncio
async def test_check_get_user_from_db_by_tg_id(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)

    async with db.session_factory() as db_session:
        user = await get_user_from_db_by_tg_id(default_user_username_inp.id, db_session)
        assert default_user_username_inp.id == user.telegram_id
        assert default_user_username_inp.username == user.username
        assert default_user_username_inp.full_name == user.full_name
        assert default_user_username_inp.count_votes == user.count_votes


# add_user_to_db
@pytest.mark.asyncio
async def test_check_one_user_add_to_db_func(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        test_user = await add_user_to_db(default_user_username_inp, db_session)
        assert default_user_username_inp.id == test_user.telegram_id
        assert default_user_username_inp.username == test_user.username
        assert default_user_username_inp.full_name == test_user.full_name
        assert default_user_username_inp.count_votes == test_user.count_votes


@pytest.mark.asyncio
async def test_check_one_user_add_to_db(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)
        query = select(User).filter(User.telegram_id == default_user_username_inp.id)
        result: Result = await db_session.execute(query)
        db_user = result.scalar()
        assert default_user_username_inp.id == db_user.telegram_id
        assert default_user_username_inp.username == db_user.username
        assert default_user_username_inp.full_name == db_user.full_name
        assert default_user_username_inp.count_votes == db_user.count_votes


@pytest.mark.asyncio
async def test_check_one_user_add_to_db_func_usrname(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        test_user = await add_user_to_db(default_user_username_inp, db_session)
        assert default_user_username_inp.id == test_user.telegram_id
        assert default_user_username_inp.username == test_user.username
        assert default_user_username_inp.full_name == test_user.full_name
        assert default_user_username_inp.count_votes == test_user.count_votes


@pytest.mark.asyncio
async def test_check_one_user_add_to_db_usrname(db, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        await add_user_to_db(default_user_username_inp, db_session)
        query = select(User).filter(User.telegram_id == default_user_username_inp.id)
        result: Result = await db_session.execute(query)
        db_user = result.scalar()
        assert default_user_username_inp.id == db_user.telegram_id
        assert default_user_username_inp.username == db_user.username
        assert default_user_username_inp.full_name == db_user.full_name
        assert default_user_username_inp.count_votes == db_user.count_votes
