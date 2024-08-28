#TODO:
# 1. Check data_pusher.contestants_push for created contestants in db
# 2. Check contestants crud
# 3. Check user crud
# 4. Check votes crud
import pytest



from database.crud.asset import (
    get_all_assets,
    get_all_assets_types,
    get_asset_by_id,
    get_list_of_asset_types,
    read_asset_field,
)
from database.crud.favorite import get_user_favorite_assets
from database.crud.openai_cost import get_user_openai_usage, insert_openai_cost
from database.crud.user import read_user_field
from database.crud.user_message_history import (
    get_last_messages,
    get_last_user_messages,
    insert_bot_message,
    insert_user_message,
)
from database.crud.utm import get_last_utm_group_id
from database.database_connector import DatabaseConnector
from database.enums import Role
from database.models import Asset, Client, Favorite, UTM, User


async def populate_db(dc: DatabaseConnector):
    async with dc.session_factory.begin() as db_session:
        db_session.add(User(user_id=1, user_first_name="vasya", user_invited_by=0, user_tg_id=5555555))
        await db_session.flush()
        db_session.add(UTM(user_id=1, group_id=1, utm_type='invited_by', utm_payload='5555555'))
        db_session.add(UTM(user_id=1, group_id=2, utm_type='asset', utm_payload='3432'))
        db_session.add(UTM(user_id=1, group_id=2, utm_type='ads', utm_payload='google'))
        db_session.add(UTM(user_id=1, group_id=3, utm_type='asset', utm_payload='344532'))
        db_session.add(UTM(user_id=1, group_id=3, utm_type='ads', utm_payload='telegram'))
        db_session.add(
            Client(
                client_id=1,
                client_tg_id=55,
                client_name='Alex Villas',
                client_description='ALEX VILLAS — это группа компаний на рынке недвижимости Бали.\n\n'
                '8 лет опыта, 3500 отзывов на AirBNB, 78 инвесторов и 176 объектов в работе',
                client_tg_first_name='Joe',
                client_years_on_market=8,
                client_objects_under_construction=176,
                client_objects_done=60,
                client_total_objects_area=550000,
                client_assets_type='1, 8',
                client_logo='logo.JPEG',
                client_presentation_link='PyCharm_cheat_sheet.pdf',
                client_video='IMG_1908.MOV',
            )
        )
        await db_session.flush()
        db_session.add(
            Asset(
                asset_id=1,
                client_id=1,
                asset_type='1, 3',
                # asset_type_id=1,
                asset_completion_year='Q1 2025',
                asset_area_sqm=400,
                asset_description='Комплекс рядом с модными местами Чангу – Finns Beach Club, Atlas Beach Club и шикарными пляжами.',
                asset_rooms_details='1br / studio / 2br',
                asset_payment_conditions='рассрочка (первоначальный взнос 25%), рассрочка 20/20, 100% оплата, крипта',
                asset_developer='Alex Villas',
                asset_title='Вилла I',
                asset_price=1000000,
                currency='USD',
                asset_location=1,
                asset_vk_link='vk.com',
                asset_building_status='presales',
                asset_price_min=10000,
                asset_price_max=1000000,
                asset_google_map_link='https://www.google.com/maps',
                asset_photos='0.jpg, 1.jpg, 2.jpg',
                asset_website_link='https://www.google.com/',
            )
        )
        db_session.add(
            Asset(
                asset_id=2,
                client_id=1,
                asset_type='1, 3',
                # asset_type_id=1,
                asset_completion_year='Q3 2026',
                asset_area_sqm=500,
                asset_description='Современный жилой комплекс с видом на море, вблизи пляжей и развлекательных центров.',
                asset_rooms_details='1br / 2br / 3br / 4br',
                asset_payment_conditions='рассрочка на 5 лет, 100% оплата, криптовалюта',
                asset_developer='SeaView Construction',
                asset_title='Вилла II',
                asset_price=2000000,
                currency='USD',
                asset_location=2,
                asset_vk_link='vk.com',
                asset_building_status='presales',
                asset_price_min=20000,
                asset_price_max=100000000,
                asset_google_map_link='https://www.google.com/maps',
                asset_photos='0.jpg, 1.jpg, 2.jpg',
                asset_website_link='https://www.google.com/',
            )
        )
        db_session.add(
            Asset(
                asset_id=3,
                client_id=1,
                asset_type='1, 3',
                # asset_type_id=1,
                asset_completion_year='Q3 2027',
                asset_area_sqm=300,
                asset_description='ипотека, рассрочка на 10 лет, 100% оплата, банковский перевод.',
                asset_rooms_details='1br / 2br',
                asset_payment_conditions='рассрочка на 5 лет, 100% оплата, криптовалюта',
                asset_developer='Urban Developers',
                asset_title='Вилла III',
                asset_price=200000,
                currency='USD',
                asset_location=2,
                asset_vk_link='vk.com',
                asset_building_status='presales',
                asset_price_min=20000,
                asset_price_max=1000000,
                asset_google_map_link='https://www.google.com/maps',
                asset_photos='0.jpg, 1.jpg, 2.jpg',
                asset_website_link='https://www.google.com/',
            )
        )
        await db_session.flush()

        db_session.add(Favorite(favorite_user_id=1, favorite_asset_id=1))
        db_session.add(Favorite(favorite_user_id=1, favorite_asset_id=2))


@pytest.mark.asyncio
async def test_get_all_assets(db):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        assets = await get_all_assets(session)
    assert len(assets) == 3


@pytest.mark.asyncio
async def test_get_asset_by_id(db: DatabaseConnector):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        asset_1 = await get_asset_by_id(1, session)
    assert asset_1.title == 'Вилла I'


@pytest.mark.asyncio
async def test_get_all_assets_types(db: DatabaseConnector):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        asset_types = await get_all_assets_types(session)
    assert len(asset_types) == 7


@pytest.mark.asyncio
async def test_get_list_of_asset_types(db):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        asset_types = await get_list_of_asset_types('1, 2', session)
    assert asset_types == ['villa', 'penthouse']


@pytest.mark.asyncio
async def test_get_last_utm_group_id(db):
    await populate_db(db)
    async with db.session_factory() as session:
        assert await get_last_utm_group_id(session) == 3


@pytest.mark.asyncio
async def test_get_user_favorite_assets(db):
    await populate_db(db)
    async with db.session_factory() as session:
        assert await get_user_favorite_assets(1, session) == {1, 2}


@pytest.mark.asyncio
async def test_insert_messages(db):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        await insert_user_message(1, 1, 1, 1, 'test user', Role.USER, session)
        await insert_bot_message(1, 1, 1, 1, 'test assistant', Role.ASSISTANT, session)
    async with db.session_factory.begin() as session:
        last_messages = await get_last_messages(session, 1)
        assert last_messages == [
            {'role': 'assistant', 'content': 'test assistant'},
            {'role': 'user', 'content': 'test user'},
        ]
        user_last_messages = await get_last_user_messages(session, 1)
        assert user_last_messages == [
            {'role': 'user', 'content': 'test user'},
        ]


@pytest.mark.asyncio
async def test_openai_cost(db):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        await insert_openai_cost(1, 1, 1, 2, 'test model', Decimal(2.0), session)
    async with db.session_factory.begin() as session:
        cost = await get_user_openai_usage(1, session)
        assert cost == {'total_tokens': 2, 'total_usd_cost': Decimal(2.0)}


@pytest.mark.asyncio
async def test_get_fields(db):
    await populate_db(db)
    async with db.session_factory.begin() as session:
        assert await read_user_field(5555555, 'user_first_name', session) == 'vasya'
        assert await read_asset_field(3, 'asset_completion_year', session) == 'Q3 2027'
