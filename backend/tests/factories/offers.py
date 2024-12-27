import factory

from src.infrastructure.models.offers import Image, Offer, Feedback, Price
from tests.factories.base import AsyncFactory


class OfferFactory(AsyncFactory):
    class Meta:
        model = Offer

    owner_id = 1
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    offer_type = 'hotel'
    phone = '+12512630796'
    city = factory.Faker('city')


class ImageFactory(AsyncFactory):
    class Meta:
        model = Image

    offer_id = 1
    data = factory.Faker('image_url')


class PriceFactory(AsyncFactory):
    class Meta:
        model = Price

    offer_id = 1
    per_hour = 100
    per_day = 1000
    per_month = 10000
    per_year = 100000


class FeedbackFactory(AsyncFactory):
    class Meta:
        model = Feedback

    user_id = 1
    offer_id = 1
    rating = 5
    text = factory.Faker('sentence')
