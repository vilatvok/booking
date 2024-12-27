from redis.asyncio import Redis
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.application.interfaces.repositories.base import (
    IRedisRepository,
    ISqlRepository,
)
from src.application.exceptions import NotFoundError, RepositoryError
from src.infrastructure.repositories.uow import SqlAlchemyUnitOfWork


def switch_model(model):
    def decorator(func):
        async def wrapper(self, data: dict):
            original_model = self.model
            self.model = model
            response = await func(self, data)
            self.model = original_model
            return response
        return wrapper
    return decorator


class SQLAlchemyRepository(ISqlRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session
        self.uow = SqlAlchemyUnitOfWork(session)

    async def add(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        return await self.get_scalar(stmt)

    async def update(self, data: dict, **kwargs):
        stmt = (
            update(self.model).
            values(**data).
            filter_by(**kwargs).
            returning(self.model)
        )
        return await self.get_scalar(stmt)

    async def delete(self, object_id: int):
        stmt = delete(self.model).where(self.model.id == object_id)
        await self.session.execute(stmt)

    async def retrieve(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        return await self.get_scalar(query)

    async def list(self):
        query = select(self.model)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_scalar(self, query):
        try:
            response = await self.session.execute(query)
            return response.scalar_one().to_entity()
        except IntegrityError as e:
            raise RepositoryError(str(e))
        except NoResultFound as e:
            raise NotFoundError(f'{self.model.__name__} not found')


class RedisRepository(IRedisRepository):
    def __init__(self, session: Redis):
        self.session = session

    async def sadd(self, key: str, data: dict):
        await self.session.sadd(key, data)

    async def smembers(self, key: str):
        return await self.session.smembers(key)
