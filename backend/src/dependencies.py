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
from src.schemas.users import UserSchema
from src.schemas.enterprises import EnterpriseSchema


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session

session = Annotated[AsyncSession, Depends(get_async_session)]


def get_redis_session():
    return Redis(connection_pool=redis_connection_pool())


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
    db: session,
    user_token: Annotated[str, Depends(user_oauth2_scheme)],
    enterprise_token: Annotated[str, Depends(enterprise_oauth2_scheme)],
    rdb = Depends(get_redis_session),
):
    # Get token data 
    data = JWT.decode_token(user_token, rdb=rdb)
    obj_type = data.get('obj')
    obj_name = data.get('name')

    match obj_type:
        case 'user':
            query = select(User).where(User.username == obj_name)
            user = (await db.execute(query)).scalar()
            return UserSchema(**user.__dict__)
        case 'google_user':
            query = select(User).where(User.username == obj_name)
            user = (await db.execute(query)).scalar()
            return UserSchema(**user.__dict__)
        case 'enterprise':
            query = select(Enterprise).where(Enterprise.name == obj_name)
            enterprise = (await db.execute(query)).scalar()
            return EnterpriseSchema(**enterprise.__dict__)
        case '_':
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


async def get_service_dependency(db: session, service_id: int):
    query = select(Service).where(Service.id == service_id)
    service = (await db.execute(query)).scalar()
    if not service:
        raise not_found
    return service


current_service = Depends(get_service_dependency)
current_user = Depends(get_current_user)
anonymous_user = Depends(get_anonymous_user)
