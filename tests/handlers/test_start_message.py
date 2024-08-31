from unittest.mock import AsyncMock, Mock

import pytest

from bot.handlers.base_handlers import start_message
from bot.internal.hello_img import hello_img
from database.models import User
from tests.default_entity_db.user import get_defult_user_list


@pytest.mark.asyncio
async def test_start_handler(default_user: User):
    message = AsyncMock()
    result = Mock()
    result.scalars.return_value.all.return_value = get_defult_user_list()
    db_session = AsyncMock()
    db_session.execute.return_value = result
    await start_message(message, default_user, db_session)
    called_args, called_kwargs = message.answer_photo.call_args
    assert called_kwargs['photo'] == hello_img


#    assert called_kwargs['text'] == expected_message
#    result.scalar.assert_called_once_with()
#    db_session.execute.assert_called_once()
#    state.clear.assert_called_once_with()
