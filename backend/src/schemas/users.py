import json

from pydantic import BaseModel, ConfigDict, model_validator, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseUser):
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


class UserSocialRegister(BaseUser):
    social_id: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

