from fastapi.testclient import TestClient

from src.main import app
from src.dependencies import get_async_session

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker


client = TestClient(app)


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    url=DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session():
    with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_session] = get_session


def test_get_services():
    response = client.get('/services/')
    assert response.status_code == 200
    assert response.json() == []
