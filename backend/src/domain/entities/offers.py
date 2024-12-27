from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.base import Entity


class OfferType(Enum):
    hotel = 'hotel'
    apartment = 'apartment'


@dataclass
class Offer(Entity):
    name: str
    description: str
    offer_type: OfferType
    city: str
    phone: str
    created_at: datetime
    owner_id: int


@dataclass
class Image(Entity):
    offer_id: int
    data: str


@dataclass
class Price(Entity):
    offer_id: int
    per_hour: float
    per_day: float
    per_month: float
    per_year: float


@dataclass
class Feedback(Entity):
    user_id: int
    offer_id: int
    created_at: datetime
    rating: int
    text: str
