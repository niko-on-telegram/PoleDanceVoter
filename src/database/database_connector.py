from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine)

from config import settings


class DatabaseConnector:
    def __init__(
            self,
            url: str,
            echo: bool = False
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


def get_db() -> DatabaseConnector:
    return DatabaseConnector(
        url=settings.postgres_db_url,
        echo=settings.echo
    )
