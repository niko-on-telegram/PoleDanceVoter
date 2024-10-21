import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.hello_img import logo_label
from bot.keyboards.contestant_choose import contestant_keyboard
from bot.keyboards.contestant_list import get_contestant_list
from database.crud.contestant import get_all_contestants, get_competitor_from_db, get_resource
from database.crud.votes import get_all_votes_ids


async def print_profile(message: Message, contestant_id: int, db_session: AsyncSession, state: FSMContext):
    contestant = await get_competitor_from_db(contestant_id, db_session)

    photos_list = [InputMediaPhoto(media=photo) for photo in contestant.photos.split(', ')]
    msg_list = []
    message = await message.answer_photo(contestant.poster)
    msg_list.append(message.message_id)
    messages = await message.answer_media_group(media=photos_list)
    msg_list.extend(message.message_id for message in messages)
    message = await message.answer(contestant.info)
    msg_list.append(message.message_id)
    message = await message.answer_video(contestant.presentation)
    msg_list.append(message.message_id)
    message = await message.answer_video(contestant.dance_cut)
    msg_list.append(message.message_id)

    already_voted = False
    voters = await get_all_votes_ids(message.chat.id, db_session)
    for voter in voters:
        if voter.competitor_id == contestant_id:
            already_voted = True

    reply_markup = contestant_keyboard(contestant_id, already_voted)

    message = await message.answer_video(contestant.dance_uncut, reply_markup=reply_markup)
    msg_list.append(message.message_id)

    logging.debug(f"{message.chat.id=} {msg_list=}")
    await state.update_data(msg_ids=msg_list)


async def print_constestant_list(message: Message, db_session: AsyncSession):
    intro_text = """<b>Приветствуем тебя на проекте ПИЛОНиЯ ищет презентёров!</b>

    В первый тур прошли ТОП-30 участников, но во второй - попадут только 20. 
    Кто это будет, решать только вам, зрителям проекта. 

    <b>Правила голосования.</b> 
    Необходимо проголосовать за 3х участников, кого Вы считаете достойным пройти в следующий этап. 
    Если Вы проголосовали меньше чем за троих, Ваши голоса НЕ будут учитываться.
    Переголосовывать НЕЛЬЗЯ.

    Окончание голосования будет 29.10 в 23:59:59. 
    Результаты озвучим 31.10

    Так же, вы можете задать вопрос участнику и посмотреть ответы. 

    Напоминаем вам, что среди тех активных зрителей, кто сделал репост сториз с конкурсом в нашем инст и проголосует на всех этапах, мы разыграем путёвку в Лагерь."""

    contestants = await get_all_contestants(db_session)
    logo_id = await get_resource(logo_label, db_session)
    await message.answer_photo(
        photo=logo_id,
        caption=intro_text,
        reply_markup=get_contestant_list(contestants),
    )
