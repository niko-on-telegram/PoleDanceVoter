from aiogram.fsm.state import StatesGroup, State


class StatesBot(StatesGroup):
    INPUT_QUESTION = State()
    ANSWER_QUESTION = State()
