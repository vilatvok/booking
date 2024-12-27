import pytest

from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy.pool import NullPool

from src.infrastructure.config import get_test_database_url
from src.infrastructure.database import (
    DatabaseSessionManager,
    get_async_session,
    get_redis_session,
)
from src.infrastructure.models.base import Base
from src.presentation.api.main import app

from tests.factories.users import CompanyFactory, UserFactory
from tests.factories.chats import ChatFactory, MessageFactory
from tests.factories.offers import (
    OfferFactory,
    ImageFactory,
    PriceFactory,
    FeedbackFactory,
)   


# Database setup
session_manager = DatabaseSessionManager(
    host=get_test_database_url(),
    engine_kwargs={'poolclass': NullPool},
)


async def get_test_session():
    async with session_manager.session() as session:
        yield session


app.dependency_overrides[get_async_session] = get_test_session
app.dependency_overrides[get_redis_session] = (
    lambda: Redis(host='redis', port=6379, db=1)
)


@pytest.fixture(autouse=True)
async def set_session_for_factories():
    async with session_manager.session() as session:
        UserFactory._meta.sqlalchemy_session = session
        CompanyFactory._meta.sqlalchemy_session = session
        ChatFactory._meta.sqlalchemy_session = session
        MessageFactory._meta.sqlalchemy_session = session
        OfferFactory._meta.sqlalchemy_session = session
        ImageFactory._meta.sqlalchemy_session = session
        PriceFactory._meta.sqlalchemy_session = session
        FeedbackFactory._meta.sqlalchemy_session = session
        yield


@pytest.fixture(autouse=True)
async def prepare_database(set_session_for_factories):
    engine = session_manager._engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='function')
async def generate_records(prepare_database):
    user = await UserFactory(username='admin')
    second_user = await UserFactory()
    await CompanyFactory(user_id=user.id)

    chat = await ChatFactory(first_user_id=user.id, second_user_id=second_user.id)
    await MessageFactory(sender_id=user.id, chat_id=chat.id)

    offer = await OfferFactory(owner_id=user.id)
    await ImageFactory(offer_id=offer.id)
    await PriceFactory(offer_id=offer.id)
    await FeedbackFactory(offer_id=offer.id, user_id=user.id)
    yield


@pytest.fixture
async def get_token():
    transport = ASGITransport(app=app)
    base_url = 'http://test'
    async with AsyncClient(transport=transport, base_url=base_url) as c:
        user = await UserFactory(username='admin')
        input_data = {
            'username': user.username,
            'password': 'ybdaa0tit',
        }
        response = await c.post('/auth/login', data=input_data)
        assert response.status_code == 200, response.json()

        # return access token
        access_token = response.json()['access_token']
        yield f'Bearer {access_token}'


@pytest.fixture
async def c():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as ac:
        yield ac


@pytest.fixture
async def ac(get_token):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
        headers={'Authorization': get_token},
    ) as c:
        yield c
