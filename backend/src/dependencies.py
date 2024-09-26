from typing import Annotated, AsyncGenerator

from fastapi import HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session_manager
from src.utils.tokens import JWT
from src.models.users import User
from src.models.enterprises import Enterprise
from src.schemas.users import UserSchema
from src.schemas.enterprises import EnterpriseSchema


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session


session = Annotated[AsyncSession, Depends(get_async_session)]


user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/users/login',
    scheme_name='user_oauth2',
)

enterprise_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/enterprises/login',
    scheme_name='enterprise_oauth2',
)


async def get_current_user(
    db: session,
    user_token: Annotated[str, Depends(user_oauth2_scheme)],
    enterprise_token: Annotated[str, Depends(enterprise_oauth2_scheme)],
):
    # Get token data
    data = JWT.decode_token(user_token)
    username = data.get('username')
    # Get user or enterprise
    if username:
        stmt = select(User).where(User.username == username)
        user = (await db.execute(stmt)).scalar()
        return UserSchema(**user.__dict__)
    elif data.get('enterprise'):
        enterprise = data.get('enterprise')
        stmt = select(Enterprise).where(Enterprise.name == enterprise)
        enterprise = (await db.execute(stmt)).scalar()
        return EnterpriseSchema(**enterprise.__dict__)
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


current_user = Depends(get_current_user)
anonymous_user = Depends(get_anonymous_user)
