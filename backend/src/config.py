from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str

    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    # Database
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_test_db: str

    # Email
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


def get_test_database_url():
    settings = get_settings()
    db = settings.postgres_test_db
    user = settings.postgres_user
    password = settings.postgres_password
    host = settings.postgres_host
    return f"postgresql+asyncpg://{user}:{password}@{host}/{db}"
