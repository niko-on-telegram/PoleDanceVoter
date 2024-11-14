from datetime import datetime

from sqlalchemy import BigInteger, MetaData, String, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class User(Base):
    __tablename__ = "users"

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


class Resource(Base):
    __tablename__ = "resources"

    label: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    file_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)


class Competitor(Base):
    __tablename__ = "competitors"

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    full_name: Mapped[str | None]
    poster: Mapped[str | None]
    photos: Mapped[str | None]
    info: Mapped[str | None]
    presentation: Mapped[str | None]
    dance_cut: Mapped[str | None]
    dance_uncut: Mapped[str | None]
    video_mid: Mapped[str | None]
    video_pro: Mapped[str | None]
    count_votes: Mapped[int] = mapped_column(default=0)

    def __str__(self):
        return (
            f"Competitor(telegram_id={self.telegram_id}, "
            f"full_name={self.full_name}, "
            f"count_votes={self.count_votes}), "
        )

    def __repr__(self):
        return self.__str__()


class Votes(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("user_id", "competitor_id"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    competitor_id: Mapped[int] = mapped_column(ForeignKey("competitors.telegram_id", ondelete="CASCADE"))
    vote_state: Mapped[str]

    def __str__(self):
        return (
            f"Voter(user_id={self.user_id}, " f"competitor_id={self.competitor_id}, " f"vote_state={self.vote_state}, "
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.user_id == other.user_id
            and self.competitor_id == other.competitor_id
            and self.vote_state == other.vote_state
        )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id", ondelete="CASCADE"))
    competitor_id: Mapped[int] = mapped_column(ForeignKey("competitors.telegram_id", ondelete="CASCADE"))
    question: Mapped[str | None]
    answer: Mapped[str | None]
    state: Mapped[int]

    def __str__(self):
        return (
            f"Questions(id={self.id}, user_id={self.user_id}, "
            f"user_id={self.user_id}, "
            f"competitor_id={self.competitor_id}, "
            f"question={self.question}, "
            f"answer={self.answer}, "
            f"state={self.state}, "
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.user_id == other.user_id
            and self.competitor_id == other.competitor_id
            and self.question == other.question
            and self.answer == other.answer
            and self.state == other.state
        )
