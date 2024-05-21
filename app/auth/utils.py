import jwt

from uuid import UUID
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext

from app.database import session
from app.auth.models import User, Enterprise
from app.auth.schemas import Token, UserRegister, EnterpriseRegister


SECRET = 'dc9af13f8be66af4d21a51441df6751f'

password_hash = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def authenticate_user(
    password: str,
    db: session,
    username: str = None,
    user_id: int = None,
):
    if username:
        query = (await db.execute(
            select(User).
            where(User.username == username)
        )).scalar()
    else:
        query = (await db.execute(
            select(User).
            where(User.id == user_id)
        )).scalar()
    if not query or not password_hash.verify(password, query.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
        )
    return query


async def authenticate_enterprise(uuid: UUID, password: str, db: session):
    try:
        query = (await db.execute(
            select(Enterprise).
            where(Enterprise.id == UUID(uuid))
        )).scalar()
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Incorrect uuid')
    else:
        if not query or not password_hash.verify(password, query.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect uuid or password',
            )
        return query


def validation_password(password: str):
    if len(password) < 8:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Too short password')
    if str(password).isalpha() or str(password).isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password must contain digits and characters',
        )


def create_token(data: dict):
    to_encode = data.copy()
    time_exp = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({'exp': time_exp})
    encoded = jwt.encode(to_encode, key=SECRET, algorithm='HS256')
    return encoded


def create_login_response(token: str):
    content = Token(token=token)
    response = JSONResponse(content=content.model_dump())
    response.set_cookie(key='jwt_token', value=token, max_age=600)
    return response


async def create_register_response(
    obj: UserRegister | EnterpriseRegister,
    avatar: str,
    class_name: str,
    db: session,
):
    if avatar.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(400, 'Invalid content type')

    if class_name == 'User':
        msg = 'User with this username exists'
        obj_class = User
        folder = 'app/users/media/users/'
        path = folder + avatar.filename
        ava = {'avatar': path}
    else:
        msg = 'Enterprise with this name exists'
        obj_class = Enterprise
        folder = 'app/users/media/enterprises/'
        path = folder + avatar.filename
        ava = {'logo': path}

    with open(path, 'wb') as f:
        f.write(await avatar.read())

    validation_password(obj.password)
    password = password_hash.hash(obj.password)
    try:
        await db.execute(
            insert(obj_class).
            values(
                {
                    **obj.model_dump(exclude=['password']),
                    **ava,
                    'password': password,
                }
            )
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg,
        )
    else:
        await db.commit()
    return {'status': 'success'}
