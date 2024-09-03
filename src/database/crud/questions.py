from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Questions


async def get_all_questions(contestant_id: int, db_session: AsyncSession) -> list[str]:
    # query = select(Questions).filter(Questions.contestant_id == contestant_id)
    # result = await db_session.execute(query)
    # list_questions = result.scalars().all()

    list_questions = [
        f"<b>Сколько?</b>",
        f"Много",
        f"<b>Здесь мог бы быть большой большой вопроссс?</b>",
        f"Здесь мог бы быть большой ответ",
        f"<b>Здесь мог бы быть большой большой вопроссс боооооооооооооольььььььььььььььшеееееееееееееееееееееееееее?</b>",
        f"Здесь мог бы быть большой ответ бббббббббооооооооооооольшееееееееееееееееееееееееееееееееееее",
        f"<b>Я вопрос</b>",
        f"А я ответ",
        f"<b>А я иной вопрос</b>",
        f"А я иной ответ",
    ]
    return list_questions


async def add_question_to_db(contestant_id: int, user_id: int, question: str, db_session: AsyncSession):
    new_question = Questions(contestant_id=contestant_id, user_id=user_id, question=question)
    db_session.add(new_question)
    await db_session.flush()
