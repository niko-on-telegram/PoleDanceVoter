from datetime import datetime

from sqlalchemy import BigInteger, MetaData, String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import settings


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(
        naming_convention=settings.naming_convention,
    )
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(String(32))
    count_votes: Mapped[int]

    def __str__(self):
        return (
            f"User(fullname={self.fullname}, "
            f"telegram_id={self.telegram_id}, "
            f"username={self.username}, "
            f"count_votes={self.count_votes})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        res = self.telegram_id == other.telegram_id
        res = res and (self.fullname == other.fullname)
        res = res and (self.count_votes == other.count_votes)
        if self.username and other.username:
            res = res and (self.username == other.username)
        return res


class Contestant(Base):
    __tablename__ = 'contestants'

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    fullname: Mapped[str]
    count_votes: Mapped[int]
    description: Mapped[str]
    video_first: Mapped[str]
    video_second: Mapped[str]
    video_third: Mapped[str]

    def __str__(self):
        return (
            f"Contestant(telegram_id={self.telegram_id}, "
            f"fullname={self.fullname}, "
            f"count_votes={self.count_votes}), "
            f"video_first={self.video_first}), "
            f"video_second={self.video_second}), "
            f"video_third={self.video_third}), "
            f"description={self.description})"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        res = self.telegram_id == other.telegram_id
        res = res and (self.fullname == other.fullname)
        res = res and (self.count_votes == other.count_votes)
        res = res and (self.video_first == other.video_first)
        res = res and (self.video_second == other.video_second)
        res = res and (self.video_third == other.video_third)
        res = res and (self.description == other.description)
        return res


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
        res = self.user_id == other.user_id
        res = res and (self.contestant_id == other.contestant_id)
        res = res and (self.vote_state == other.vote_state)
        return res
