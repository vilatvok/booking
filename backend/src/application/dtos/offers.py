import json

from datetime import datetime
from pydantic import BaseModel, Field, model_validator, field_validator
from pydantic_extra_types import phone_numbers

from src.domain.entities.offers import OfferType


class OfferPrices(BaseModel):
    per_hour: float | None = 0
    per_day: float | None = 0
    per_month: float | None = 0
    per_year: float | None = 0

    @field_validator("per_hour", "per_day", "per_month", "per_year")
    def ensure_non_negative(cls, value):
        if value < 0:
            raise ValueError("Price values must be non-negative")
        return value


class ImageSchema(BaseModel):
    data: str


class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    text: str


class FeedbackSchema(FeedbackCreate):
    id: int
    user: str
    created_at: datetime


class OfferCreate(BaseModel):
    name: str = Field(..., min_length=4, max_length=50)
    description: str
    offer_type: OfferType
    city: str
    phone: phone_numbers.PhoneNumber
    prices: OfferPrices | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class OfferCreateOutput(OfferCreate):
    id: int
    images: list[ImageSchema]


class OfferSchema(OfferCreateOutput):
    owner: str


class OfferUpdate(OfferCreate):
    name: str | None = Field(None, min_length=4, max_length=50)
    description: str | None = None
    offer_type: OfferType | None = None
    city: str | None = None
    phone: phone_numbers.PhoneNumber | None = None
    prices: OfferPrices | None = None


class OfferUnitSchema(OfferSchema):
    feedbacks: list[FeedbackSchema] = []
    avg_rating: float | None = None
