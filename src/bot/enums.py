from enum import IntEnum, auto


class ContestantEnum(IntEnum):
    PROFILE = auto()
    VOTE = auto()
    QUESTION = auto()
    CHECK_ANSWER = auto()
    BACK = auto()


class VotesEnum(IntEnum):
    VOTE = auto()
    BACK = auto()
