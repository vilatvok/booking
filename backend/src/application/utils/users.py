import bcrypt

from src.application.utils.common import generate_image_path
from src.application.exceptions import InvalidDataError, ValidationError


class PasswordService:

    @staticmethod
    def validate(password: str) -> None:
        if len(password) < 8:
            raise ValidationError('Too short password')
        if password.isalpha() or password.isdigit():
            raise ValidationError('Password must contain digits and characters')

    @staticmethod
    def hash(password: str) -> bytes:
        pwd_bytes = password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed

    @classmethod
    def check(cls, password: str, hashed_password: str) -> None:
        cls.validate(password)
        pwd_bytes = password.encode()
        user_pwd_bytes = hashed_password.encode()
        is_verified = bcrypt.checkpw(pwd_bytes, user_pwd_bytes)
        if not is_verified:
            raise InvalidDataError('Invalid password')

    @classmethod
    def generate(cls, password: str) -> str:
        cls.validate(password)
        hashed_password = cls.hash(password)
        return hashed_password.decode()


async def prepare_image_data(file: dict) -> str:
    image = file['image']
    path = file['path'] + image.filename
    return await generate_image_path(
        path=path,
        image=image,
        content_type=image.content_type,
    )
