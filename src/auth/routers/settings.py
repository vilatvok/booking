from typing import Annotated

from fastapi import Depends, status, APIRouter

from sqlalchemy import update

from src.database import session
from src.auth import schemas, utils
from src.auth.models import User, Enterprise
from src.auth.dependencies import current_user, oauth2_scheme
from src.auth.config import redis_client


router = APIRouter()


@router.patch('/change_password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    db: session,
    user: Annotated[User | Enterprise, current_user],
    password_form: schemas.PasswordChange,
):
    username = user.get('username')
    enterprise_id = user.get('enter_id')
    if user:
        await utils.authenticate_user(
            db=db,
            username=username,
            password=password_form.old_password,
        )
        utils.validate_password(password_form.new_password)
        password = utils.password_hash.hash(password_form.new_password)
        await db.execute(
            update(User).
            values(password=password).
            where(User.username == username)
        )
    else:
        await utils.authenticate_enterprise(
            db=db,
            uuid=enterprise_id,
            password=password_form.old_password,
        )
        utils.validate_password(password_form.new_password)
        password = utils.password_hash.hash(password_form.new_password)
        await db.execute(
            update(Enterprise).
            values(password=password).
            where(Enterprise.id == enterprise_id)
        )
    await db.commit()
    return {'status': 'changed'}


@router.post('/logout', dependencies=[current_user])
async def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    redis_client.sadd('jwt_blacklist', token)
    return {'status': 'You logged out'}
