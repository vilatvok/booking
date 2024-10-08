from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select, update, and_
from sqlalchemy.exc import IntegrityError

from src.dependencies import session
from src.utils.common import generate_image_path
from src.utils.tokens import JWT
from src.models.users import User
from src.models.enterprises import Enterprise
from src.celery import (
    delete_inactive_enterprise,
    delete_inactive_user,
    send_confirmation_letter,
)


class Password:
    password_hash = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @staticmethod
    def validate(password: str):
        password_unique_msg = 'Password must contain digits and characters'
        too_short_msg = 'Too short password'
        if len(password) < 8:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, too_short_msg)
        if password.isalpha() or password.isdigit():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, password_unique_msg)

    @classmethod
    def hash(cls, password: str):
        return cls.password_hash.hash(password)

    @classmethod
    def check(cls, password: str, current_password: str):
        cls.validate(password)
        is_verified = cls.password_hash.verify(password, current_password)
        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect password',
            )

    @classmethod
    def generate(cls, password: str):
        cls.validate(password)
        return cls.hash(password)


class BaseAuth:
    @staticmethod
    async def generate_data(form: dict, file: dict | None = None):
        data = form.model_dump()
        data['password'] = Password.generate(form.password)
        if file:
            path = file['path']
            image = file['image']
            file_type = file['type']
            data[file_type] = await generate_image_path(path, image)
        return data

    @staticmethod
    async def insert_data(db: session, obj: User | Enterprise, data: dict):
        try:
            db.add(obj(**data))
            await db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{obj.__class__} already exists.'
            )
        
    @staticmethod
    def object_exists(msg: str, obj: User | Enterprise | None):
        exc = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Incorrect {msg}',
        )
        if obj is None:
            raise exc


class AuthUser(BaseAuth):
    @classmethod
    async def registration(cls, db: session, form: dict, image):
        if image:
            avatar = {
                'path': 'media/users/',
                'type': 'avatar',
                'image': image,
            }
        else:
            avatar = None
        data = await cls.generate_data(form, avatar)
        await cls.insert_data(db, User, data)

        # run celery tasks
        send_confirmation_letter.apply_async(args=[
            form.username,
            form.email,
            'users',
        ])
        delete_inactive_user.apply_async(args=[form.username])
        return {'status': 'Check your email for confirmation letter.'}

    @staticmethod
    async def confirm_registration(token: str, db: session):
        data = JWT.decode_token(token)
        username = data['name']

        query = select(User).where(User.username == username)
        user = (await db.execute(query)).scalar()
        if not user or user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is not found or already exists.'
            )

        await db.execute(
            update(User).
            where(User.username == username).
            values(is_active=True)
        )
        await db.commit()
        return {'status': 'User has been created successfully'}

    @classmethod
    async def authenticate(cls, db: session, username: str, password: str):
        query = (
            select(User).
            where(and_(
                User.username == username,
                User.provider == 'local',
                User.is_active == True
            ))
        )
        user = (await db.execute(query)).scalar()

        cls.object_exists('username', user)     
        Password.check(password, user.password)
        return user


class AuthEnterprise(BaseAuth):
    @classmethod
    async def registration(cls, db: session, form: dict, image=None):
        if image:
            logo = {
                'path': 'media/enterprises/',
                'type': 'logo',
                'image': image,
            }
        else:
            logo = None
        data = await cls.generate_data(form, logo)
        await cls.insert_data(db, Enterprise, data)

        # run celery tasks
        send_confirmation_letter.apply_async(args=[
            form.name,
            form.email,
            'enterprises',
        ])
        delete_inactive_enterprise.apply_async(args=[form.name])
        return {'status': 'Check your email for confirmation letter.'}

    @staticmethod
    async def confirm_registration(token: str, db: session):
        data = JWT.decode_token(token)
        name = data['name']

        query = select(Enterprise).where(Enterprise.name == name)
        enterprise = (await db.execute(query)).scalar()
        print(enterprise)
        if not enterprise or enterprise.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Enterprise is not found or already exists.'
            )

        await db.execute(
            update(Enterprise).
            where(Enterprise.name == name).
            values(is_active=True)
        )
        await db.commit()
        return {'status': 'Enterprise has been created successfully'}

    @classmethod
    async def authenticate(cls, db: session, email: str, password: str):
        enterprise = (await db.execute(
            select(Enterprise).
            where(Enterprise.email == email, Enterprise.is_active == True)
        )).scalar()

        cls.object_exists('email', enterprise)
        Password.check(password, enterprise.password)
        return enterprise
