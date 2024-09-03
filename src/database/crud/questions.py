import aiogram
from aiogram.utils.formatting import Bold
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_questions(contestant_id: int, db_session: AsyncSession) -> list[str]:
    # query = select(Questions).filter(Questions.contestant_id == contestant_id)
    # result = await db_session.execute(query)
    # list_questions = result.scalars().all()

    list_questions = [
        "Сколько?",
        "Много",
        "Здесь мог бы быть большой большой вопроссс?",
        "Здесь мог бы быть большой ответ",
        "Здесь мог бы быть большой большой вопроссс боооооооооооооольььььььььььььььшеееееееееееееееееееееееееее?",
        "Здесь мог бы быть большой ответ бббббббббооооооооооооольшееееееееееееееееееееееееееееееееееее",
        "Я вопрос",
        "А я ответ",
        "А я иной вопрос",
        "А я иной ответ",
    ]
    return list_questions
