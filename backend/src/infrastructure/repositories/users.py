from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from src.application.interfaces.repositories.users import (
    ICompanyRepository,
    IUserRepository,
)
from src.infrastructure.repositories.base import SQLAlchemyRepository
from src.infrastructure.models.users import Company, User
from src.infrastructure.models.offers import Offer


class UserRepository(SQLAlchemyRepository, IUserRepository):
    model = User

    async def get_user_offers(self, username: str):
        query = (
            select(self.model).
            where(self.model.username == username).
            options(
                joinedload(self.model.offers).joinedload(Offer.prices),
                joinedload(self.model.offers).joinedload(Offer.images)
            )
        )
        offers = await self.session.execute(query)
        return offers.unique().scalar_one()


class CompanyRepository(SQLAlchemyRepository, ICompanyRepository):
    model = Company

    async def get_company_offers(self, name: str):
        query = (
            select(self.model).
            where(self.model.name == name).
            options(
                joinedload(self.model.user).
                joinedload(User.offers).
                joinedload(Offer.prices),
                joinedload(self.model.user).
                joinedload(User.offers).
                joinedload(Offer.images)
            )
        )
        return await self.get_scalar(query)
    
    async def get_user_company(self, user_id: int):
        query = select(self.model).where(self.model.user_id == user_id)
        return await self.get_scalar(query)

    async def delete(self, object_id: int):
        async with self.uow:
            stmt = delete(self.model).where(self.model.user_id == object_id)
            await self.session.execute(stmt)
        return {'status': 'Deleted'}
