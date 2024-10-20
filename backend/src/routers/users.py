from typing import Annotated

from fastapi import Form, status, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.datastructures import UploadFile
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload

from src.exceptions import not_found
from src.utils.common import generate_image_path
from src.utils.services import get_obj_services
from src.utils.tokens import JWT
from src.utils.auth import AuthUser
from src.models.users import User
from src.models.services import Service
from src.schemas.tokens import Token
from src.schemas.users import UserRegister, UserSchema
from src.schemas.services import ServiceSchema
from src.dependencies import (
    anonymous_user,
    current_user,
    redis_session,
    user_oauth2_scheme,
    db_session,
)


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[anonymous_user],
    status_code=status.HTTP_200_OK,
)
async def registration(
    db: db_session,
    form: UserRegister,
    avatar: UploadFile | None = None,
):
    return await AuthUser.registration(db, form, avatar)


@router.get(
    path='/register-confirm/{token}',
    dependencies=[anonymous_user],
    status_code=status.HTTP_201_CREATED,
)
async def confirm_registration(token: str, db: db_session):
    return await AuthUser.confirm_registration(token, db)


@router.post(
    path='/login',
    dependencies=[anonymous_user],
    response_model=Token,
)
async def login(
    db: db_session,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await AuthUser.authenticate(db, form.username, form.password)
    data = {'obj': 'user', 'id': user.id, 'name': user.username}
    access = JWT.create_token(data)
    refresh = JWT.create_token(data, exp_time=1440)
    return Token(access_token=access, refresh_token=refresh)


@router.get('/', response_model=list[UserSchema])
async def get_users(db: db_session):
    users = (await db.execute(select(User))).scalars().all()
    return users


@router.get('/{username}', response_model=UserSchema)
async def get_user(db: db_session, username: str):
    query = select(User).where(User.username == username)
    user = (await db.execute(query)).scalar()
    if not user:
        raise not_found
    return user


@router.get('/{username}/services', response_model=list[ServiceSchema])
async def get_user_services(db: db_session, username: str):
    query = (
        select(User).
        where(User.username == username).
        options(
            joinedload(User.services).joinedload(Service.prices),
            joinedload(User.services).joinedload(Service.images)
        )
    )
    services = (await db.execute(query)).scalar()
    if not services:
        raise not_found

    return get_obj_services(services)


@router.patch('/me', status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    db: db_session,
    current_user: Annotated[UserSchema, current_user],
    username: Annotated[str | None, Form()] = None,
    email: Annotated[str | None, Form()] = None,
    avatar: UploadFile | None = None,
):  
    data = {}
    if username:
        data['username'] = username
    if email:
        data['email'] = email
    if avatar:
        path = 'media/users/'
        ava = await generate_image_path(path, avatar)
        data['avatar'] = ava

    stmt = (
        update(User).
        values(data).
        where(User.id == current_user.id).
        returning(User.id)
    )
    
    obj = await db.execute(stmt)
    if not obj.fetchone():
        raise not_found

    await db.commit()
    return {'status': 'Updated'}


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: db_session,
    rdb: redis_session,
    current_user: Annotated[UserSchema, current_user],
    token: Annotated[str, Depends(user_oauth2_scheme)],
):
    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()

    rdb.sadd('jwt_blacklist', token)

    return {'status': 'Deleted'}
