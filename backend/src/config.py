from functools import lru_cache

import redis

from pydantic_settings import BaseSettings


redis_client = redis.Redis(host='redis',decode_responses=True)


class Settings(BaseSettings):
    secret_key: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    email_host_user: str
    email_host_password: str


@lru_cache
def get_settings():
    return Settings()


def get_database_url():
    settings = get_settings()
    db = settings.postgres_db
    user = settings.postgres_user
    password = settings.postgres_password
    host = settings.postgres_host
    return f"postgresql+asyncpg://{user}:{password}@{host}/{db}"