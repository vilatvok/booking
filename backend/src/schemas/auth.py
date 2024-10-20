import enum

from pydantic import BaseModel, EmailStr


class ObjType(enum.Enum):
    user = 'user'
    enterprise = 'enterprise'


class PasswordReset(BaseModel):
    model: ObjType
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    password1: str
    password2: str

