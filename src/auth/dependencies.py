from typing import Annotated

from fastapi import HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select

from src.database import session
from src.auth.models import User
from src.auth.utils import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


async def get_current_user(
    db: session, 
    token: Annotated[str, Depends(oauth2_scheme)],
):
    data = decode_token(token)
    username = data.get('username')
    enterprise_id = data.get('enterprise_id')
    
    if username:
        user = (await db.execute(
            select(User).
            where(User.username == username)
        )).scalar()
        return user
    elif enterprise_id:
        return {'enterprise_id': enterprise_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid data',
            headers={'WWW-Authenticate': 'Bearer'},
        )


def get_anonymous_user(request: Request):
    data = request.cookies.get('jwt', None)
    if data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't register/login while you are logged in",
        )


current_user = Depends(get_current_user)
anonymous_user = Depends(get_anonymous_user)
