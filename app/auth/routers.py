from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Response, Request, UploadFile, status

from sqlalchemy import select, update

from app.database import session
from app.exceptions import not_found
from app.auth import schemas, utils
from app.auth.models import User, Enterprise
from app.auth.dependencies import current_user, anonym_user


user_router = APIRouter()
enterprise_router = APIRouter()
settings_router = APIRouter()


# User routers
###############################################################################

@user_router.post(
    '/register', 
    dependencies=[anonym_user], 
    status_code=status.HTTP_201_CREATED
)
async def user_register(
    user: Annotated[schemas.UserRegister, Body()],
    avatar: UploadFile,
    db: session
):
    result = await utils.create_register_response(user, avatar, User.__name__, db)
    return result


@user_router.post('/login', dependencies=[anonym_user])
async def user_login(user: schemas.UserLogin, db: session):
    user = await utils.authenticate_user(user.password, db, username=user.username)
    token = utils.create_token(data={'user_id': user.id})
    response = utils.create_login_response(token)
    return response


@user_router.get(
    '/{username}', 
    response_model=schemas.User, 
)
async def get_user(username: str, db: session):
    query = (await db.execute(
        select(User).
        where(User.username == username)
    )).scalar()
    if not query:
        raise not_found
    return query


# Enterprise routers
###############################################################################

@enterprise_router.post(
    '/register',
    dependencies=[anonym_user], 
    status_code=status.HTTP_201_CREATED
)
async def enterprise_register(
    enterprise: Annotated[schemas.EnterpriseRegister, Body()], 
    avatar: UploadFile, 
    db: session
):
    result = await utils.create_register_response(
        enterprise, 
        avatar, 
        Enterprise.__name__,
        db
    )
    return result


@enterprise_router.post('/login', dependencies=[anonym_user])
async def enterprise_login(enterprise: schemas.EnterpriseLogin, db: session):
    enterprise = await utils.authenticate_enterprise(
        enterprise.id, 
        enterprise.password, 
        db
    )
    token = utils.create_token(data={'enter_id': str(enterprise.id)})
    response = utils.create_login_response(token)
    return response


@enterprise_router.get(
    '/{name}', 
    response_model=schemas.Enterprise,
)
async def get_enterprise(name: str, db: session):
    query = (await db.execute(
        select(Enterprise).
        where(Enterprise.name == name)
    )).scalar()
    if not query:
        raise not_found
    return query


# Settings routers
###############################################################################

@settings_router.patch('/change_password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    password_form: schemas.PasswordChange,
    user: Annotated[User | Enterprise, current_user],
    db: session
):
    user_id = user.get('user_id')
    enterprise_id = user.get('enter_id')
    if user:
        await utils.authenticate_user(password_form.old_password, db, id=user_id)
        utils.validation_password(password_form.new_password)
        password = utils.password_hash.hash(password_form.new_password)
        await db.execute(
            update(User).
            values(password=password).
            where(User.id == user_id)
        )
    else:
        await utils.authenticate_enterprise(
            enterprise_id, 
            password_form.old_password, 
            db
        )
        utils.validation_password(password_form.new_password)
        password = utils.password_hash.hash(password_form.new_password)
        await db.execute(
            update(Enterprise).
            values(password=password).
            where(Enterprise.id == enterprise_id)
        )
    await db.commit()
    return {'status': 'changed'}


@settings_router.post('/logout', dependencies=[current_user])
async def logout(request: Request, response: Response):
    token = request.cookies.get('jwt_token')
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    response.delete_cookie('jwt_token')
    return {'status': 'You logged out'}