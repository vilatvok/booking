from abc import abstractmethod

from src.application.interfaces.repositories.base import ISqlRepository


class IUserRepository(ISqlRepository):

    @abstractmethod
    async def get_user_offers(self, name: str):
        raise NotImplementedError


class ICompanyRepository(ISqlRepository):

    @abstractmethod
    async def get_company_offers(self, name: str):
        raise NotImplementedError

    @abstractmethod
    async def get_user_company(self, user_id: int):
        raise NotImplementedError
