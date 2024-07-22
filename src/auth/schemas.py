import json

from uuid import UUID
from pydantic import BaseModel, model_validator, EmailStr
from datetime import date


class BaseUser(BaseModel):
    username: str
    email: EmailStr | None = None


class User(BaseUser):
    id: int
    avatar: str


class UserRegister(BaseUser):
    password: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class EnterpriseRegister(BaseModel):
    name: str
    owner: str
    email: EmailStr
    password: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Enterprise(BaseModel):
    id: UUID
    name: str
    logo: str
    email: EmailStr
    owner: str
    created: date


class EnterpriseLogin(BaseModel):
    email: EmailStr
    password: str
