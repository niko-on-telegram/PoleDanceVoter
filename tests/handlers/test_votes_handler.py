from unittest.mock import AsyncMock, Mock

import pytest
from aiogram.types import InputMediaVideo

from bot.handlers.votes_handler import callback_back, callback_vote


@pytest.mark.asyncio
async def test_callback_back(
    default_contestants_list, default_user, default_votes_callback_factory_back, default_contestant_keyboard
):
    result = Mock()
    result.scalars.return_value.all.return_value = default_contestants_list
    db_session = AsyncMock()
    db_session.execute.return_value = result
    message = AsyncMock()
    callback = AsyncMock()
    callback.message = message
    callback_back_data = default_votes_callback_factory_back
    await callback_back(callback=callback, callback_data=callback_back_data, db_session=db_session)
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


@pytest.mark.asyncio
async def test_callback_vote_more_3(default_user_list, default_votes_callback_factory_vote):
    result = Mock()
    result.scalar.return_value = default_user_list[1]
    db_session = AsyncMock()
    db_session.execute.return_value = result
    message = AsyncMock()
    callback = AsyncMock()
    callback.answer = "Вы уже проголосовали допустимое количество раз!"
    callback.message = message
    callback_back_data = default_votes_callback_factory_vote
    await callback_vote(callback=callback, callback_data=callback_back_data, db_session=db_session)


@pytest.mark.asyncio
async def test_callback_vote_second_for_one(default_user_list, default_votes_callback_factory_vote):
    result = Mock()
    result.scalar.return_value = default_user_list[1]
    db_session = AsyncMock()
    db_session.execute.return_value = result
    message = AsyncMock()
    callback = AsyncMock()
    callback.answer = "Вы уже проголосовали допустимое количество раз!"
    callback.message = message
    callback_back_data = default_votes_callback_factory_vote
    await callback_vote(callback=callback, callback_data=callback_back_data, db_session=db_session)