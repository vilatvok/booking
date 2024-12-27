from typing import Annotated
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer

from src.application.dtos.users import UserComplete
from src.presentation.api.dependencies.usecases import user_usecase


user_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    scheme_name='user_oauth2',
)


async def get_current_user(
    token: Annotated[str, Depends(user_oauth2_scheme)],
    user_usecase: user_usecase,
):
    token_data = await user_usecase.get_user_data(token)
    username = token_data.get('username')
    username = await user_usecase.get_user(username)
    return UserComplete(**username.__dict__)


def get_anonymous_user(request: Request):
    """Generally is used for registration and login routes."""

    token = request.headers.get('Authorization')
    if not token:
        return
    elif token.startswith('Bearer'):
        raise PermissionError('You are already logged in')


current_user = Depends(get_current_user)
anonymous_user = Depends(get_anonymous_user)
