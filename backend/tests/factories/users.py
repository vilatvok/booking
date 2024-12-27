import factory

from src.application.utils.users import PasswordService
from src.infrastructure.models.users import User, Company
from tests.factories.base import AsyncFactory


class UserFactory(AsyncFactory):
    class Meta:
        model = User
        sqlalchemy_get_or_create = ['username']

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: PasswordService.generate('ybdaa0tit'))
    is_active = True


class CompanyFactory(AsyncFactory):
    class Meta:
        model = Company
        sqlalchemy_get_or_create = ['name']

    user_id = 1
    name = factory.Faker('name')
    email = factory.Faker('email')
    owner = factory.Faker('name')
