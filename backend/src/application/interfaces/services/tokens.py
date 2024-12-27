from abc import ABC, abstractmethod
from redis.asyncio import Redis


class ITokenService(ABC):
    @abstractmethod
    def encode(self, data: dict, exp_time: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def decode(self, token: str, rdb: Redis | None = None) -> dict:
        raise NotImplementedError
