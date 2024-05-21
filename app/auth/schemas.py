import json
from uuid import UUID
from pydantic import BaseModel, model_validator
from datetime import date


class BaseUser(BaseModel):
    username: str
    email: str | None = None


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
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    token: str


class EnterpriseRegister(BaseModel):
    name: str
    owner: str
    created: date
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
    owner: str
    created: date


class EnterpriseLogin(BaseModel):
    id: str
    password: str
