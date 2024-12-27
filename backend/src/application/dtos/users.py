from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class BaseUser(BaseModel):
    username: str = Field(..., min_length=4, max_length=20)
    email: EmailStr


class UserSchema(BaseUser):
    id: int
    avatar: str
    provider: str


class UserComplete(UserSchema):
    password: str | None = None
    is_active: bool


class UserRegister(BaseUser):
    avatar: UploadFile | None = None
    password: str = Field(..., min_length=8)


class UserSocialRegister(BaseUser):
    social_id: str
    avatar: str | None = None


class UserUpdate(BaseUser):
    username: str | None = Field(None, min_length=4, max_length=20)
    email: EmailStr | None = None
    avatar: UploadFile | None = None


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    password1: str = Field(..., min_length=8)
    password2: str = Field(..., min_length=8)


class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RefreshToken(BaseModel):
    refresh_token: str
    username: str | None = None
