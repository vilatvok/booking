import json
import pytest


@pytest.mark.parametrize('path, status', [
    ('/offers/', 200),
    ('/offers/1', 200),
])
async def test_get_offer(c, path, status):
    response = await c.get(path)
    assert response.status_code == status, response.json()


async def test_create_offer(ac):
    data = {
        'name': 'Test offer',
        'description': 'Test description',
        'offer_type': 'hotel',
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
            'test.png', open('tests/images/test.png', 'rb'),
            'image/png'
        )
    }

    response = await ac.post(
        url='/offers/',
        data={'form_data': json.dumps(data)},
        files=files,
    )

    assert response.status_code == 201, response.json()


async def test_update_offer(ac):
    response = await ac.patch('/offers/1', json={'name': 'Test 2'})
    assert response.status_code == 202, response.json()


async def test_create_feedback(ac):
    data = {'rating': 5, 'text': 'Test feedback'}
    response = await ac.post('/offers/1/feedback', json=data)
    assert response.status_code == 201, response.json()


async def test_delete_offer(ac):
    response = await ac.delete('/offers/1')
    assert response.status_code == 204, response.json()
