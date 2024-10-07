import json
import pytest

from sqlalchemy import select

from src.models.services import Service
from tests.conftest import session_manager


@pytest.mark.parametrize('path, status', [
    ('/services/', 200),
    ('/services/1', 404),
])
async def test_get_service_routers(c, path, status):
    response = await c.get(path)
    assert response.status_code == status


async def test_create_service(auc):
    data ={
        'name': 'Test service',
        'description': 'Test description',
        'type': 'hotel',
        'city': 'Test city',
        'phone': '+380971234567',
        'prices': {
            'per_hour': 100,
            'per_day': 500,
            'per_month': 1500,
            'per_year': 18000,
        }
    }
    files = {
        'images': (
            's.png', open('tests/images/s.png', 'rb'),
            'image/png'
        )
    }

    response = await auc.post(
        url='/services/',
        data={'service': json.dumps(data)},
        files=files,
    )

    assert response.status_code == 201
    assert response.json() == {'status': 'Ok'}


async def test_update_service(auc):
    response = await auc.patch('/services/1', json={'name': 'Test 2'})
    assert response.status_code == 202
    
    async with session_manager.session() as session:
        service = await session.execute(
            select(Service).
            where(Service.id == 1)
        )
        service = service.scalar()
        assert service.name == 'Test 2', service.name


async def test_create_feedback(auc):
    data = {
        'rating': 5,
        'text': 'Test feedback'
    }

    response = await auc.post('/services/1/feedback', json=data)
    assert response.status_code == 201


async def test_delete_service(auc):
    response = await auc.delete('/services/1')
    assert response.status_code == 204
