import logging
import random

from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.hello_img import logo_label
from bot.keyboards.contestant_choose import contestant_keyboard
from bot.keyboards.contestant_list import get_contestant_list
from config import settings
from database.crud.contestant import get_all_contestants, get_resource
from database.crud.votes import get_all_votes_ids
from database.models import Competitor


async def print_profile(message: Message, contestant: Competitor, db_session: AsyncSession, state: FSMContext):
    photos_list = [InputMediaPhoto(media=photo) for photo in contestant.photos.split(", ")]
    msg_list = []
    message = await message.answer_photo(contestant.poster)
    msg_list.append(message.message_id)
    messages = await message.answer_media_group(media=photos_list)
    msg_list.extend(message.message_id for message in messages)
    message = await message.answer(contestant.info)
    msg_list.append(message.message_id)
    message = await message.answer_video(contestant.presentation, protect_content=True)
    msg_list.append(message.message_id)
    message = await message.answer_video(contestant.dance_cut, protect_content=True)
    msg_list.append(message.message_id)
    message = await message.answer_video(contestant.dance_uncut, protect_content=True)
    msg_list.append(message.message_id)
    message = await message.answer_video(contestant.video_mid, protect_content=True)
    msg_list.append(message.message_id)

    voters = await get_all_votes_ids(message.chat.id, db_session)
    if len(voters) >= settings.VOTE_LIMIT:
        show_vote_btn = False
    else:
        show_vote_btn = not any(voter.competitor_id == contestant.telegram_id for voter in voters)

    reply_markup = contestant_keyboard(contestant.telegram_id, show_vote_btn)

    message = await message.answer_video(contestant.video_pro, protect_content=True)
    msg_list.append(message.message_id)

    message = await message.answer_video(contestant.video_3rd_tour, reply_markup=reply_markup, protect_content=True)
    msg_list.append(message.message_id)

    logging.debug(f"{message.chat.id=} {msg_list=}")
    await state.update_data(msg_ids=msg_list)


async def print_constestant_list(message: Message, db_session: AsyncSession):
    main_message = """Это ФИНАЛ! 🔥🔥🔥

Начинаем решающий этап голосования, по итогам которого станут известны имена победителей! 👑

Здесь ты можешь просмотреть всю информацию об участницах, а также их выступление на чемпионате Платинум!

❤️ Голосовать можно только за одну из девушек! 
👉 Приниматься голоса будут от зрителей, которые подписаны на наш ТГ канал @pdcamp

❤️‍🔥 Голосование продлится до 13 декабря – не упусти возможность поддержать своего фаворита! ❤️‍🔥"""

    contestants = await get_all_contestants(db_session)
    random.Random(hash(message.chat.id)).shuffle(contestants)
    logo_id = await get_resource(logo_label, db_session)
    await message.answer_photo(
        photo=logo_id,
        caption=main_message,
        reply_markup=get_contestant_list(contestants),
    )
