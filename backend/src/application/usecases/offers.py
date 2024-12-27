from src.application.interfaces.repositories.offers import IOfferRepository
from src.application.dtos.offers import (
    FeedbackCreate,
    OfferCreate,
    OfferSchema,
    OfferUnitSchema,
    OfferUpdate,
    OfferCreateOutput,
)
from src.application.utils.common import generate_image_path
from src.application.utils.offers import format_offer


class OfferUseCase:

    def __init__(self, repository: IOfferRepository):
        self.repository = repository

    async def create_offer(self, user_id: int, offer: OfferCreate, images: list):
        async with self.repository.uow:
            # Save offer
            offer_data = offer.model_dump(exclude=['prices'])
            offer_data['owner_id'] = user_id
            offer_response = await self.repository.add(offer_data)
            offer_id = offer_response.id

            # Save prices
            price_data = offer.prices.model_dump()
            price_data['offer_id'] = offer_id
            prices = await self.repository.add_prices(price_data)

            # Save images
            images_input = []
            folder = 'media/offers/'
            for image in images:
                img_path = folder + image.filename
                path = await generate_image_path(
                    path=img_path,
                    image=image,
                    content_type=image.content_type,
                )
                image_data = {'data': path, 'offer_id': offer_id}
                images_input.append(image_data)

            images_db_response = await self.repository.add_images(images_input)
            images_response = [image.to_dict() for image in images_db_response]

        response = offer_response.to_dict()
        response['images'] = images_response
        response['prices'] = prices.to_dict()
        return OfferCreateOutput(**response)

    async def get_offer(self, offer_id: int):
        offer, avg_rating = await self.repository.retrieve(id=offer_id)
        response_data = format_offer(offer)

        # Get feedbacks
        feedbacks = []
        for feedback in offer.feedbacks:
            feedback_entity = feedback.to_entity()
            feedback_to_dict = feedback_entity.to_dict()
            feedback_to_dict['user'] = feedback.user.username
            feedbacks.append(feedback_to_dict)

        response_data['feedbacks'] = feedbacks
        response_data['avg_rating'] = avg_rating
        return OfferUnitSchema(**response_data)

    async def get_offers(self):
        offers = await self.repository.list()
        response_data = []
        for offer in offers:
            response_data.append(OfferSchema(**format_offer(offer)))
        return response_data

    async def update_offer(self, offer_id: int, data: OfferUpdate):
        offer_data = data.model_dump(exclude=['prices'], exclude_unset=True)
        prices_data = data.prices.model_dump(exclude_unset=True)
        response = {}
        async with self.repository.uow:
            if offer_data:
                offer = await self.repository.update(offer_data, id=offer_id)
                response = offer.to_dict()
            if data.prices:
                filter_by = {'offer_id': offer_id}
                prices = await self.repository.update_prices(prices_data, filter_by)
                response['prices'] = prices.to_dict()
        return OfferUpdate(**response)

    async def delete_offer(self, offer_id: int):
        async with self.repository.uow:
            await self.repository.delete(offer_id)
        return {'status': 'Deleted'}

    async def create_feedback(self, data: dict):
        async with self.repository.uow:
            response = await self.repository.add_feedback(data)
        return FeedbackCreate(**response.to_dict())
