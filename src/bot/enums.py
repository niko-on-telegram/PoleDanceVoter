from enum import IntEnum, auto


class ContestantEnum(IntEnum):
    PROFILE = auto()
    VOTE = auto()
    QUESTION = auto()
    CHECK_ANSWER = auto()
    BACK = auto()
    DELETE = auto()


class VotesEnum(IntEnum):
    VOTE = auto()
    BACK = auto()


class QuestionState(IntEnum):
    QUESTION = auto()
    MODERATION = auto()
    MODERATION_REJECT = auto()
    WAITING_RESPONSE = auto()
    REJECTED = auto()
    ANSWERED = auto()


class QuestionBack(IntEnum):
    BACK = auto()
