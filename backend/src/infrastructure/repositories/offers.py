from sqlalchemy import insert, select, func
from sqlalchemy.orm import joinedload

from src.application.exceptions import NotFoundError
from src.application.interfaces.repositories.offers import IOfferRepository
from src.infrastructure.repositories.base import SQLAlchemyRepository, switch_model
from src.infrastructure.models.offers import Image, Offer, Feedback, Price


class OfferRepository(SQLAlchemyRepository, IOfferRepository):
    model = Offer

    async def list(self) -> list:
        query = (
            select(self.model).
            options(
                joinedload(self.model.owner),
                joinedload(self.model.images),
                joinedload(self.model.prices),
            )
        )
        offers = await self.session.execute(query)
        return offers.unique().scalars().all()

    async def retrieve(self, **kwargs):
        avg_rating = func.round(func.avg(Feedback.rating), 1).label('avg_rating')
        query = (
            select(self.model, avg_rating).
            filter_by(**kwargs).
            outerjoin(self.model.feedbacks).
            options(
                joinedload(self.model.owner),
                joinedload(self.model.prices),
                joinedload(self.model.images),
                joinedload(self.model.feedbacks).joinedload(Feedback.user),
            ).
            group_by(self.model)
        )
        res = await self.session.execute(query)
        try:
            offer, avg_rating = res.first()
        except TypeError:
            raise NotFoundError('Offer not found')
        return offer, avg_rating

    @switch_model(Price)
    async def add_prices(self, data: dict):
        return await self.add(data)

    @switch_model(Image)
    async def add_images(self, data: list):
        stmt = insert(self.model).values(data).returning(self.model)
        images = await self.session.execute(stmt)
        return [image.to_entity() for image in images.scalars().all()]

    @switch_model(Feedback)
    async def add_feedback(self, data: dict):
        return await self.add(data)

    @switch_model(Price)
    async def update_prices(self, data: dict, **kwargs):
        return await self.update(data, **kwargs)
