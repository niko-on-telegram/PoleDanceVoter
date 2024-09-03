from unittest.mock import AsyncMock, Mock

import pytest

from bot.handlers.base_handlers import start_message
from bot.internal.hello_img import hello_img
from database.models import User


@pytest.mark.asyncio
async def test_start_handler(default_user: User, default_contestants_list, default_contestants_kb):
    message = AsyncMock()
    result = Mock()
    result.scalars.return_value.all.return_value = default_contestants_list
    db_session = AsyncMock()
    db_session.execute.return_value = result
    await start_message(message, default_user, db_session)
    called_args, called_kwargs = message.answer_photo.call_args
    assert called_kwargs['photo'] == hello_img
    assert called_kwargs['caption'] == f'Hello, {default_user.full_name}. Список участников:'
    assert called_kwargs['reply_markup'] == default_contestants_kb
