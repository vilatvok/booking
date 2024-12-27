from typing import Annotated
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases.offers import OfferUseCase
from src.application.usecases.users import (
    UserSocialUseCase,
    UserUseCase,
    CompanyUseCase,
)
from src.application.usecases.chats import ChatUseCase
from src.infrastructure.config import get_settings
from src.infrastructure.database import get_async_session, get_redis_session
from src.infrastructure.repositories.base import RedisRepository
from src.infrastructure.repositories.offers import OfferRepository
from src.infrastructure.repositories.users import (
    CompanyRepository,
    UserRepository,
)
from src.infrastructure.repositories.chats import ChatRepository
from src.infrastructure.services.tokens import JWTService
from src.infrastructure.services.tasks import BackgroundTasksService


db_session = Annotated[AsyncSession, Depends(get_async_session)]
redis_session = Annotated[Redis, Depends(get_redis_session)]


def prepare_usecase(func):
    def wrapper(
        db_session: db_session,
        redis_session: redis_session,
    ):
        return func(db_session, redis_session=redis_session)
    return wrapper


@prepare_usecase
def get_user_usecase(db_session: AsyncSession, **kwargs: any):
    redis_session = kwargs.get('redis_session')
    return UserUseCase(
        UserRepository(db_session),
        RedisRepository(redis_session),
        JWTService(),
        BackgroundTasksService(get_settings()),
    )


@prepare_usecase
def get_user_social_usecase(db_session: AsyncSession, **kwargs: any):
    return UserSocialUseCase(UserRepository(db_session), JWTService())


@prepare_usecase
def get_company_usecase(db_session: AsyncSession, **kwargs: any):
    return CompanyUseCase(CompanyRepository(db_session),)


@prepare_usecase
def get_offer_usecase(db_session: AsyncSession, **kwargs: any):
    return OfferUseCase(OfferRepository(db_session))


@prepare_usecase
def get_chat_usecase(db_session: AsyncSession, **kwargs: any):
    return ChatUseCase(
        ChatRepository(db_session),
        UserRepository(db_session),
        JWTService(),
    )


user_usecase = Annotated[UserUseCase, Depends(get_user_usecase)]
user_social_usecase = Annotated[UserSocialUseCase, Depends(get_user_social_usecase)]
company_usecase = Annotated[CompanyUseCase, Depends(get_company_usecase)]
offer_usecase = Annotated[OfferUseCase, Depends(get_offer_usecase)]
chat_usecase = Annotated[ChatUseCase, Depends(get_chat_usecase)]
