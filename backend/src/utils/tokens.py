import jwt

from redis import Redis
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from src.config import get_settings


settings = get_settings()


class JWT:
    @staticmethod
    def create_token(data: dict, exp_time: int = 10) -> str:
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=exp_time)
        to_encode = data.copy()
        to_encode.update({'exp': expire_at})
        encoded = jwt.encode(to_encode, key=settings.secret_key)
        return encoded

    @staticmethod
    def decode_token(token: str, rdb: Redis | None = None) -> dict:
        exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is invalid',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        # Raise an error if token is in the blacklist.
        if rdb:
            if token in rdb.smembers('jwt_blacklist'):
                raise exc

        try:
            data = jwt.decode(
                jwt=token,
                key=settings.secret_key,
                algorithms=['HS256']
            )
        except jwt.exceptions.InvalidTokenError:
            raise exc
        return data
