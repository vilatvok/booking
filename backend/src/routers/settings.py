from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import update

from src.models.enterprises import Enterprise
from src.models.users import User
from src.utils.tokens import JWT
from src.utils.auth import Password
from src.schemas.settings import PasswordChange
from src.schemas.users import UserComplete
from src.schemas.enterprises import EnterpriseComplete
from src.dependencies import (
    current_user,
    user_oauth2_scheme,
    enterprise_oauth2_scheme,
    db_session,
    redis_session,
)


router = APIRouter()


@router.put('/password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    db: db_session,
    current_user: Annotated[UserComplete | EnterpriseComplete, current_user],
    password_form: PasswordChange,
):
    obj = User if isinstance(current_user, UserComplete) else Enterprise

    Password.check(password_form.old_password, current_user.password)
    password = Password.hash(password_form.new_password)

    await db.execute(
        update(obj).
        values(password=password).
        where(current_user.id == current_user.id)
    )
    await db.commit()
    return {'status': 'changed'}


@router.post('/logout', dependencies=[current_user])
async def logout(
    rdb: redis_session,
    user_token: Annotated[str, Depends(user_oauth2_scheme)],
    enterprise_token: Annotated[str, Depends(enterprise_oauth2_scheme)],
):
    try:
        JWT.decode_token(user_token)
        token = user_token
    except HTTPException:
        token = enterprise_token

    # Add token to blacklist
    rdb.sadd('jwt_blacklist', token)
    return {'status': 'You logged out'}
