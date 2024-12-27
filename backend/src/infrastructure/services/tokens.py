import jwt

from datetime import datetime, timedelta, timezone
from redis.asyncio import Redis

from src.application.exceptions import InvalidDataError
from src.infrastructure.config import get_settings


settings = get_settings()


class JWTService:

    @staticmethod
    def encode(data: dict, exp_time: int = 10) -> str:
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=exp_time)
        to_encode = data.copy()
        to_encode.update({'exp': expire_at})
        encoded = jwt.encode(to_encode, key=settings.secret_key)
        return encoded

    @staticmethod
    async def decode(token: str, rdb: Redis | None = None) -> dict:
        if rdb:
            if token in await rdb.smembers('jwt_blacklist'):
                raise InvalidDataError('Token is in the blacklist')
        try:
            data = jwt.decode(token, key=settings.secret_key, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            raise InvalidDataError('Invalid token')
        return data
