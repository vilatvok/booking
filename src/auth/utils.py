import jwt

from datetime import datetime, timedelta, UTC

from fastapi import HTTPException, status
from fastapi.datastructures import UploadFile

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from passlib.context import CryptContext

from src.database import session
from src.auth import config
from src.auth.models import User, Enterprise
from src.auth.schemas import UserRegister, EnterpriseRegister
from src.auth.config import redis_client


password_hash = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_token(data: dict):
    expire_at = datetime.now(UTC) + timedelta(minutes=10)
    to_encode = data.copy()
    to_encode.update({'exp': expire_at})
    encoded = jwt.encode(to_encode, key=config.SECRET, algorithm='HS256')
    return encoded


def decode_token(token):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Token is invalid',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    if token in redis_client.smembers('jwt_blacklist'):
        raise exc
    try:
        data = jwt.decode(
            jwt=token,
            key=config.SECRET,
            algorithms=['HS256']
        )
    except jwt.exceptions.InvalidTokenError:
        raise exc
    return data


async def authenticate_user(db: session, username: str, password: str):
    user = (await db.execute(
        select(User).
        where(User.username == username)
    )).scalar()
    if not user or not password_hash.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password',
        )
    return user


async def authenticate_enterprise(db: session, email: str, password: str):
    try:
        enterprise = (await db.execute(
            select(Enterprise).
            where(Enterprise.email == email)
        )).scalar()
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Incorrect email address')
    else:
        is_verified = password_hash.verify(password, enterprise.password)
        if not enterprise or not is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect email or password',
            )
        return enterprise


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Too short password')
    if str(password).isalpha() or str(password).isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password must contain digits and characters',
        )


async def register_response(
    db: session,
    obj: UserRegister | EnterpriseRegister,
    obj_class: User | Enterprise,
    avatar: UploadFile | None = None,
):
    # validate password data
    validate_password(obj.password)
    password = password_hash.hash(obj.password)

    data = obj.model_dump()
    data['password'] = password

    if obj_class == User:
        msg = 'User with this username exists'
        field_name = 'avatar'
        folder = r'C:\Users\kvydyk\Documents\booking\src\media\users'
    else:
        msg = 'Enterprise with this name exists'
        field_name = 'logo'
        folder = r'C:\Users\kvydyk\Documents\booking\src\media\enterprises'

    # check avatar content type
    if avatar:
        if avatar.content_type not in ['image/jpeg', 'image/png']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid content type',
            )

        path = f'{folder}\\{avatar.filename}'

        # save avatar in media
        with open(path, 'wb') as f:
            f.write(await avatar.read())

        data[field_name] = path

    try:
        await db.execute(
            insert(obj_class).
            values(data)
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg,
        )
    else:
        await db.commit()

    return {'status': 'success'}
