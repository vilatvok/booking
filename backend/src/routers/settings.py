from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import update

from src.utils.tokens import JWT
from src.utils.auth import Password
from src.schemas.enterprises import EnterpriseSchema
from src.schemas.settings import PasswordChange
from src.schemas.users import UserSchema
from src.models.users import User
from src.models.enterprises import Enterprise
from src.dependencies import (
    current_user,
    user_oauth2_scheme,
    enterprise_oauth2_scheme,
    session,
    get_redis_session,
)


router = APIRouter()


@router.patch('/change_password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    db: session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    password_form: PasswordChange,
):
    Password.check(password_form.current_password, current_user.password)

    if current_user.__class__ == User:
        password = Password.hash(password_form.new_password)
        await db.execute(
            update(User).
            values(password=password).
            where(User.username == current_user.username)
        )
    else:
        password = Password.hash(password_form.new_password)
        await db.execute(
            update(Enterprise).
            values(password=password).
            where(Enterprise.id == current_user.id)
        )
    await db.commit()
    return {'status': 'changed'}


@router.post('/logout', dependencies=[current_user])
async def logout(
    user_token: Annotated[str, Depends(user_oauth2_scheme)],
    enterprise_token: Annotated[str, Depends(enterprise_oauth2_scheme)],
    rdb = Depends(get_redis_session),
):
    try:
        JWT.decode_token(user_token)
        token = user_token
    except HTTPException:
        token = enterprise_token

    # Add token to blacklist
    rdb.sadd('jwt_blacklist', token)
    return {'status': 'You logged out'}
