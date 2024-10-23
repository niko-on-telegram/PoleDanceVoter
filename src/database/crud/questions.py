from sqlalchemy import select, Result, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Question
from bot.enums import QuestionState


async def get_all_questions(contestant_id: int, db_session: AsyncSession) -> list[str]:
    # noinspection PyTypeChecker
    query = select(Question).filter(Question.competitor_id == contestant_id)
    result = await db_session.execute(query)
    questions = result.scalars().all()
    list_questions = list()
    for it in questions:  # Берем только вопросы с ответами и выделяем вопрос жирным
        if it.state == QuestionState.ANSWERED:
            list_questions.append(f"<b>{it.question}</b>\n{it.answer}")
    return list_questions


async def add_question_to_db(
    competitor_id: int, user_id: int, question: str, state: QuestionState, db_session: AsyncSession
) -> int:
    new_question = Question(competitor_id=competitor_id, user_id=user_id, question=question, state=state)
    db_session.add(new_question)
    await db_session.flush()
    return new_question.id


async def add_answer_to_db(question_id: int, answer: str, db_session: AsyncSession):
    updates = update(Question).where(Question.id == question_id).values(answer=answer)
    await db_session.execute(updates)


async def update_state(question_id: int, state: QuestionState, db_session: AsyncSession):
    updates = update(Question).where(Question.id == question_id).values(state=state)
    await db_session.execute(updates)


async def get_state(question_id: int, db_session: AsyncSession) -> QuestionState:
    query = select(Question).filter(Question.id == question_id)
    result: Result = await db_session.execute(query)
    question = result.scalar()
    return question.state


async def get_question(question_id: int, db_session: AsyncSession) -> Question:
    query = select(Question).filter(Question.id == question_id)
    result: Result = await db_session.execute(query)
    question = result.scalar()
    return question
