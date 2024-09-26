import json
import enum
from datetime import datetime

from pydantic import BaseModel, model_validator, ConfigDict
from pydantic_extra_types import phone_numbers


class ServiceType(enum.Enum):
    hotel = 'hotel'
    apartment = 'apartment'


class ServicePrices(BaseModel):
    per_hour: float | None = 0
    per_day: float | None = 0
    per_month: float | None = 0
    per_year: float | None = 0

    model_config = ConfigDict(from_attributes=True)


class ImageSchema(BaseModel):
    data: str


class FeedbackCreate(BaseModel):
    rating: int
    text: str


class FeedbackSchema(FeedbackCreate):
    user: str
    created: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceCreate(BaseModel):
    name: str
    description: str
    type: ServiceType
    city: str
    phone: phone_numbers.PhoneNumber
    prices: ServicePrices | None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class ServiceSchema(ServiceCreate):
    id: int
    owner: str
    images: list[ImageSchema]


class ServiceUpdate(ServiceCreate):
    name: str | None = None
    description: str | None = None
    type: ServiceType | None = None
    city: str | None = None
    phone: phone_numbers.PhoneNumber | None = None
    prices: ServicePrices | None = None


class OneService(ServiceSchema):
    feedbacks: list[FeedbackSchema] = []
    avg_rating: float
