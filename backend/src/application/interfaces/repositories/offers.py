from abc import abstractmethod

from src.application.interfaces.repositories.base import ISqlRepository


class IOfferRepository(ISqlRepository):

    @abstractmethod
    async def add_prices(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def add_images(self, data: list):
        raise NotImplementedError

    @abstractmethod
    async def add_feedback(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_prices(self, data: dict, **kwargs):
        raise NotImplementedError
