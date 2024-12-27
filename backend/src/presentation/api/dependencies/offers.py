from typing import Annotated
from fastapi import Depends

from src.application.utils.offers import format_offer
from src.application.dtos.users import UserComplete
from src.application.dtos.offers import OfferSchema
from src.presentation.api.dependencies.users import current_user
from src.presentation.api.dependencies.usecases import offer_usecase


async def is_current_offer(offer_id: int, offer_usecase: offer_usecase):
    offer, _ = await offer_usecase.repository.retrieve(id=offer_id)
    return OfferSchema(**format_offer(offer))


current_offer = Depends(is_current_offer)


def is_offer_owner(
    current_user: Annotated[UserComplete, current_user],
    offer: Annotated[OfferSchema, current_offer],
):
    if current_user.username != offer.owner:
        raise PermissionError('You are not the owner of this offer')


offer_owner = Depends(is_offer_owner)
