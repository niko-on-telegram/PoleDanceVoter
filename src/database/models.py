from datetime import datetime

from sqlalchemy import BigInteger, MetaData, String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    full_name: Mapped[str]
    username: Mapped[str | None] = mapped_column(String(32))
    count_votes: Mapped[int]

    def __str__(self):
        return (
            f"User(full_name={self.full_name}, "
            f"telegram_id={self.telegram_id}, "
            f"username={self.username}, "
            f"count_votes={self.count_votes})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.telegram_id == other.telegram_id
            and self.full_name == other.full_name
            and self.count_votes == other.count_votes
            and self.username == other.username
        )


class Contestant(Base):
    __tablename__ = 'contestants'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    full_name: Mapped[str]
    count_votes: Mapped[int]
    description: Mapped[str]
    video_first: Mapped[str]
    video_second: Mapped[str]
    video_third: Mapped[str]

    def __str__(self):
        return (
            f"Contestant(telegram_id={self.telegram_id}, "
            f"full_name={self.full_name}, "
            f"count_votes={self.count_votes}), "
            f"video_first={self.video_first}), "
            f"video_second={self.video_second}), "
            f"video_third={self.video_third}), "
            f"description={self.description})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.telegram_id == other.telegram_id
            and self.full_name == other.full_name
            and self.count_votes == other.count_votes
            and self.video_first == other.video_first
            and self.video_second == other.video_second
            and self.video_third == other.video_third
            and self.description == other.description
        )


class Votes(Base):
    __tablename__ = 'votes'
    __table_args__ = (UniqueConstraint('user_id', 'contestant_id'),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    contestant_id: Mapped[int] = mapped_column(ForeignKey("contestants.telegram_id", ondelete="CASCADE"))
    vote_state: Mapped[str]

    def __str__(self):
        return (
            f"Voter(user_id={self.user_id}, " f"contestant_id={self.contestant_id}, " f"vote_state={self.vote_state}, "
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.user_id == other.user_id
            and self.contestant_id == other.contestant_id
            and self.vote_state == other.vote_state
        )


class Questions(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    contestant_id: Mapped[int] = mapped_column(ForeignKey("contestants.telegram_id", ondelete="CASCADE"))
    question: Mapped[str | None]
    answer: Mapped[str | None]

    def __str__(self):
        return (
            f"Questions(id={self.id}, user_id={self.user_id}, "
            f"user_id={self.user_id}, "
            f"contestant_id={self.contestant_id}, "
            f"question={self.question}, "
            f"answer={self.answer}, "
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.user_id == other.user_id
            and self.contestant_id == other.contestant_id
            and self.question == other.question
            and self.answer == other.answer
        )
