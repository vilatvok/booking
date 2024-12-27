from typing import Annotated
from fastapi import APIRouter, status, UploadFile

from src.application.dtos.users import UserComplete
from src.application.dtos.offers import (
    FeedbackCreate,
    OfferUnitSchema,
    OfferCreate,
    OfferCreateOutput,
    OfferSchema,
    OfferUpdate,
)
from src.presentation.api.dependencies.users import current_user
from src.presentation.api.dependencies.offers import current_offer, offer_owner
from src.presentation.api.dependencies.usecases import offer_usecase


router = APIRouter()


@router.get('/', response_model=list[OfferSchema])
async def get_offers(offer_usecase: offer_usecase):
    return await offer_usecase.get_offers()


@router.get('/{offer_id}', response_model=OfferUnitSchema)
async def get_offer(offer_id: int, offer_usecase: offer_usecase):
    return await offer_usecase.get_offer(offer_id)


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=OfferCreateOutput,
)
async def create_offer(
    current_user: Annotated[UserComplete, current_user],
    form_data: OfferCreate,
    images: list[UploadFile],
    offer_usecase: offer_usecase,
):
    return await offer_usecase.create_offer(current_user.id, form_data, images)


@router.patch(
    path='/{offer_id}',
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[offer_owner],
)
async def update_offer(
    offer: Annotated[OfferSchema, current_offer],
    form_data: OfferUpdate,
    offer_usecase: offer_usecase,
):
    return await offer_usecase.update_offer(offer.id, form_data)


@router.delete(
    path='/{offer_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[offer_owner],
)
async def delete_offer(
    offer: Annotated[OfferSchema, current_offer],
    offer_usecase: offer_usecase,
):  
    return await offer_usecase.delete_offer(offer.id)


@router.post(
    path='/{offer_id}/feedback',
    status_code=status.HTTP_201_CREATED,
    response_model=FeedbackCreate,
)
async def create_feedback(
    current_user: Annotated[UserComplete, current_user],
    offer: Annotated[OfferSchema, current_offer],
    form_data: FeedbackCreate,
    offer_usecase: offer_usecase,
):
    data = form_data.model_dump()
    data['user_id'] = current_user.id
    data['offer_id'] = offer.id
    return await offer_usecase.create_feedback(data)
