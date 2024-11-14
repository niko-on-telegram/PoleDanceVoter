from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums import QuestionState
from database.models import Question


def format_question(question: Question) -> str:
    return f"<b>{question.question}</b>\n{question.answer}"


async def get_all_questions(contestant_id: int, db_session: AsyncSession) -> list[str]:
    # noinspection PyTypeChecker
    query = select(Question).filter(Question.competitor_id == contestant_id).filter(Question.state == QuestionState.ANSWERED)
    result = await db_session.execute(query)
    list_questions = [format_question(it) for it in result.scalars().all()]
    return list_questions


async def add_question_to_db(
        competitor_id: int, user_id: int, question: str, state: QuestionState, db_session: AsyncSession,
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
