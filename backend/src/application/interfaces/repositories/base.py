from abc import ABC, abstractmethod


class ISqlRepository(ABC):

    @abstractmethod
    async def list(self):
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: dict, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, object_id: int):
        raise NotImplementedError


class IRedisRepository(ABC):

    @abstractmethod
    async def sadd(self, key: str, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def smembers(self, key: str):
        raise NotImplementedError
