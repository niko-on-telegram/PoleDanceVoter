from aiogram.fsm.state import State, StatesGroup


class StatesBot(StatesGroup):
    INPUT_QUESTION = State()
    ANSWER_QUESTION = State()
    CONFIRMING_VOTE = State()
