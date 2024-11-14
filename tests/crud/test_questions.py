import pytest

from bot.enums import QuestionState
from database.crud.questions import get_all_questions, add_question_to_db, add_answer_to_db
from database.crud.user import add_user_to_db


@pytest.mark.asyncio
async def test_get_all_questions(db, default_contestants_list, default_user_username_inp):
    async with db.session_factory.begin() as db_session:
        db_session.add_all(default_contestants_list)

    async with db.session_factory.begin() as db_session:
        new_user = await add_user_to_db(default_user_username_inp, db_session)
    async with db.session_factory.begin() as db_session:
        q_id = await add_question_to_db(default_contestants_list[0].telegram_id, new_user.telegram_id, "abacaba", QuestionState.ANSWERED, db_session)

        await add_question_to_db(default_contestants_list[0].telegram_id, new_user.telegram_id, "asdasd", QuestionState.QUESTION, db_session)

    async with db.session_factory.begin() as db_session:
        await add_answer_to_db(q_id, "asd", db_session)

    async with db.session_factory() as db_session:
        questions = await get_all_questions(default_contestants_list[0].telegram_id, db_session)
        assert len(questions) == 1
        assert questions[0] == "<b>abacaba</b>\nasd"

    async with db.session_factory() as db_session:
        questions = await get_all_questions(default_contestants_list[1].telegram_id, db_session)
        assert len(questions) == 0

