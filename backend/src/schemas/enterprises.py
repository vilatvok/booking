import json

from datetime import datetime
from pydantic import BaseModel, model_validator, EmailStr


class EnterpriseSchema(BaseModel):
    id: int
    name: str
    logo: str
    email: EmailStr
    owner: str
    created_at: datetime


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

