from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.types import InputMediaVideo

from bot.handlers.contestant_handler import callback_back, callback_profile, callback_vote
from bot.internal.hello_img import hello_img


@pytest.mark.asyncio
async def test_callback_back(
    default_contestants_list, default_contestants_kb, default_user, default_contestant_callback_factory_back
):
    result = Mock()
    result.scalars.return_value.all.return_value = default_contestants_list
    db_session = AsyncMock()
    db_session.execute.return_value = result
    message = AsyncMock()
    callback = AsyncMock()
    callback.message = message
    callback_back_data = default_contestant_callback_factory_back
    await callback_back(callback=callback, callback_data=callback_back_data, db_session=db_session, user=default_user)
    called_args, called_kwargs = callback.message.answer_photo.call_args
    assert called_kwargs['photo'] == hello_img
    assert called_kwargs['caption'] == f'{default_user.full_name}, список участников:'
    assert called_kwargs['reply_markup'] == default_contestants_kb


@pytest.mark.asyncio
async def test_callback_profile(
    default_contestants_list, default_contestant_callback_factory_profile, default_contestant_keyboard
):
    result = Mock()
    result.scalar.return_value = default_contestants_list[0]
    db_session = AsyncMock()
    db_session.execute.return_value = result
    message = AsyncMock()
    callback = AsyncMock()
    callback.message = message
    callback_back_data = default_contestant_callback_factory_profile
    await callback_profile(callback=callback, callback_data=callback_back_data, db_session=db_session)
    called_args, called_kwargs = callback.message.answer_media_group.call_args
    assert called_kwargs['protect_content'] == True
    assert called_kwargs['media'] == [
        InputMediaVideo(media=default_contestants_list[0].video_first),
        InputMediaVideo(media=default_contestants_list[0].video_second),
        InputMediaVideo(media=default_contestants_list[0].video_third),
    ]
    called_args, called_kwargs = callback.message.answer.call_args
    assert called_kwargs['text'] == default_contestants_list[0].description
    assert called_kwargs['reply_markup'] == default_contestant_keyboard


# TODO: изменить тесты под изменившуюся логику
@pytest.mark.asyncio
async def test_callback_vote(
    default_contestants_list,
    default_user,
    default_contestant_callback_factory_vote,
    default_vote_kb,
):
    result = Mock()
    result.scalar.return_value = default_contestants_list[0]
    db_session = AsyncMock()
    db_session.execute.return_value = result
    message = AsyncMock()
    callback = AsyncMock()
    callback.message = message
    callback_back_data = default_contestant_callback_factory_vote
    await callback_vote(callback=callback, callback_data=callback_back_data, db_session=db_session)
    called_args, called_kwargs = callback.message.answer.call_args
    assert (
        called_kwargs['text']
        == f"Вы уверены что хотите проголосовать за участника {default_contestants_list[0].full_name}?"
    )
    assert called_kwargs['reply_markup'] == default_vote_kb
