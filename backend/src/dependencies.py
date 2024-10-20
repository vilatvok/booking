from typing import Annotated, AsyncGenerator

from redis import Redis
from fastapi import HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import not_found
from src.models.services import Service
from src.database import redis_connection_pool, session_manager
from src.utils.tokens import JWT
from src.models.users import User
from src.models.enterprises import Enterprise
from src.schemas.users import UserComplete
from src.schemas.enterprises import EnterpriseComplete


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session

db_session = Annotated[AsyncSession, Depends(get_async_session)]


def get_redis_session() -> Redis:
    return Redis(connection_pool=redis_connection_pool())

redis_session = Annotated[Redis, Depends(get_redis_session)]


user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/users/login',
    scheme_name='user_oauth2',
)

enterprise_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/enterprises/login',
    scheme_name='enterprise_oauth2',
    description='Username here is used as email',
)


async def get_current_user(
    db: db_session,
    rdb: redis_session,
    user_token: Annotated[str, Depends(user_oauth2_scheme)],
    enterprise_token: Annotated[str, Depends(enterprise_oauth2_scheme)],
):
    # Get token data 
    data = JWT.decode_token(user_token, rdb=rdb)
    obj_type = data.get('obj')
    obj_name = data.get('name')

    if obj_type in ('user', 'google_user'):
        query = select(User).where(User.username == obj_name)
        user = (await db.execute(query)).scalar()
        if not user:
            raise HTTPException(
                detail='User is not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return UserComplete(**user.__dict__)
    elif obj_type == 'enterprise':
        query = select(Enterprise).where(Enterprise.name == obj_name)
        enterprise = (await db.execute(query)).scalar()
        if not enterprise:
            raise HTTPException(
                detail='Enterprise is not found',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return EnterpriseComplete(**enterprise.__dict__)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid data',
            headers={'WWW-Authenticate': 'Bearer'},
        )


def get_anonymous_user(request: Request):
    """Generally is used for registration and login routes."""
    token = request.headers.get('Authorization')
    if not token:
        return
    if token.startswith('Bearer'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't register/login while you are logged in",
        )


async def get_service_dependency(db: db_session, service_id: int):
    query = select(Service).where(Service.id == service_id)
    service = (await db.execute(query)).scalar()
    if not service:
        raise not_found
    return service


current_service = Depends(get_service_dependency)
current_user = Depends(get_current_user)
anonymous_user = Depends(get_anonymous_user)
