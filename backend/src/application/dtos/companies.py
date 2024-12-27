import json

from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator, EmailStr


class CompanySchema(BaseModel):
    id: int
    user_id: int
    name: str
    logo: str
    email: EmailStr
    owner: str
    created_at: datetime


class CompanyRegister(BaseModel):
    name: str = Field(..., min_length=4, max_length=30)
    owner: str = Field(..., min_length=5, max_length=40)
    email: EmailStr
    logo: UploadFile | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CompanyUpdate(BaseModel):
    name: str | None = Field(None, min_length=4, max_length=30)
    owner: str | None = Field(None, min_length=5, max_length=40)
    email: EmailStr | None = None
    logo: UploadFile | None = None
