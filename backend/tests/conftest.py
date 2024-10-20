import pytest

from httpx import ASGITransport, AsyncClient
from redis import Redis
from sqlalchemy.pool import NullPool

from src.main import app
from src.database import DatabaseSessionManager
from src.dependencies import get_async_session, get_redis_session
from src.models.common import Base
from src.models.users import User
from src.models.enterprises import Enterprise
from src.config import get_test_database_url
from src.utils.auth import Password


# Database setup
session_manager = DatabaseSessionManager(
    host=get_test_database_url(),
    engine_kwargs={'poolclass': NullPool},
)


# Override db session
async def get_test_session():
    async with session_manager.session() as session:
        yield session

app.dependency_overrides[get_async_session] = get_test_session


# Override redis module
app.dependency_overrides[get_redis_session] = (
    lambda: Redis(host='redis', port=6379, db=1)
)


# Make fixtures
@pytest.fixture(autouse=True, scope='module')
async def prepare_database():
    engine = session_manager._engine

    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # create user and enterprise
    async with session_manager.session() as session:
        hashed_password = Password.hash('12345rtx')
        user = User(
            username='admin',
            password=hashed_password,
            email='john@gmail.com',
            is_active=True,
        )
        enterprise = Enterprise(
            name='admin',
            owner='miracle',
            password=hashed_password,
            email='john@gmail.com',
            is_active=True,
        )
        session.add_all([user, enterprise])
        await session.commit()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_token(data):
    transport = ASGITransport(app=app)
    base_url = 'http://test'
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        if data == 'user':
            user_data = {'username': 'admin', 'password': '12345rtx'}
            response = await ac.post('/users/login', data=user_data)
        else:
            enterprise_data = {
                'username': 'john@gmail.com',
                'password': '12345rtx',
            }
            response = await ac.post('/enterprises/login', data=enterprise_data)
        access_token = response.json()['access_token']
        yield f'Bearer {access_token}'


async def client(headers: dict = None):
    transport = ASGITransport(app=app)
    base_url = 'http://test'
    async with AsyncClient(
        transport=transport,
        base_url=base_url,
        headers=headers,
    ) as ac:
        yield ac


@pytest.fixture(scope='module')
async def c():
    async for c in client():
        yield c


@pytest.fixture(scope='module')
async def user_token():
    async for token in get_token('user'):
        yield token


@pytest.fixture(scope='module')
async def enterprise_token():
    async for token in get_token('enterprise'):
        yield token


@pytest.fixture(scope='module')
async def auc(user_token):
    async for ac in client({'Authorization': user_token}):
        yield ac


@pytest.fixture(scope='module')
async def aec(enterprise_token):
    async for ac in client({'Authorization': enterprise_token}):
        yield ac
