import json
import enum

from datetime import datetime

from pydantic import BaseModel, model_validator
from pydantic_extra_types import phone_numbers

from sqlalchemy import Integer, TypeDecorator


class ServiceType(enum.Enum):
    hotel = 'hotel'
    apartment = 'apartment'


class Rate(enum.Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class Image(BaseModel):
    data: str


class ServicePrices(BaseModel):
    per_hour: float | None = 0
    per_day: float | None = 0
    per_month: float | None = 0
    per_year: float | None = 0

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    rating: Rate
    text: str


class Feedback(FeedbackCreate):
    user: str
    created: datetime

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    name: str
    description: str
    type: ServiceType
    city: str
    phone: phone_numbers.PhoneNumber
    prices: ServicePrices | None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        from_attributes = True


class ServiceUpdate(ServiceCreate):
    name: str | None = None
    description: str | None = None
    type: ServiceType | None = None
    city: str | None = None
    phone: phone_numbers.PhoneNumber | None = None
    prices: ServicePrices | None = None


class Service(ServiceCreate):
    id: int
    owner: str
    images: list[Image]


class ServiceOne(Service):
    feedbacks: list[Feedback] = []
    avg_rating: float
