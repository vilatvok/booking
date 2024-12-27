import contextlib

from typing import AsyncGenerator, AsyncIterator
from redis.asyncio import Redis, ConnectionPool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.config import get_database_url
    
    
class DatabaseSessionManager:

    def __init__(self, host: str, engine_kwargs: dict = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DatabaseSessionManager(host=get_database_url())

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session


async def get_redis_session() -> AsyncGenerator[Redis, None]:
    pool = ConnectionPool(host='redis', decode_responses=True)
    redis = Redis(connection_pool=pool)
    try:
        yield redis
    finally:
        await redis.aclose()
        await redis.connection_pool.disconnect()
