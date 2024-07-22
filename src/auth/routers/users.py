from typing import Annotated

from fastapi import Depends, status, APIRouter
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Body
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select, delete

from src.database import session
from src.exceptions import not_found
from src.auth import schemas, utils
from src.auth.models import User
from src.auth.dependencies import current_user, anonymous_user
from src.exceptions import permission_required, not_found


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[anonymous_user],
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    db: session,
    user: Annotated[schemas.UserRegister, Body()],
    avatar: UploadFile | None = None,
):
    result = await utils.register_response(
        db=db,
        obj=user,
        obj_class=User,
        avatar=avatar,
    )
    return result


@router.post('/login', dependencies=[anonymous_user])
async def login(
    db: session,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await utils.authenticate_user(db, form.username, form.password)
    token = utils.create_token({'username': user.username})
    return schemas.Token(access_token=token, token_type='bearer')


@router.get('/', response_model=list[schemas.User])
async def get_users(db: session):
    users = (await db.execute(select(User))).scalars().all()
    return users


@router.get('/{username}', response_model=schemas.User)
async def get_user(db: session, username: str):
    user = (await db.execute(
        select(User).
        where(User.username == username)
    )).scalar()
    if not user:
        raise not_found
    return user


@router.delete(
    path='/{username}/delete',
    dependencies=[current_user],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    db: session,
    username: str,
    current_user: Annotated[User, current_user],
):
    user = (await db.execute(
        select(User).
        where(User.username == username)
    )).scalar()

    if not user:
        raise not_found
    if username != current_user.username:
        raise permission_required

    await db.execute(delete(User).where(User.username == username))
    await db.commit()
    return {'status': 'Deleted'}
