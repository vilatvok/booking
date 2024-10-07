import json
import pytest

from unittest.mock import patch

from src.utils.tokens import JWT


@patch('src.celery.send_confirmation_letter.apply_async')
async def test_registration(mock_send_confirmation_letter, c):
    mock_send_confirmation_letter.return_value = None
    data = {
        'name': 'test_enterprise',
        'owner': 'Test owner',
        'email': 'asdvtr@gmail.com',
        'password': '123456rt'
    }

    response = await c.post(
        url='/enterprises/register',
        data={'form': json.dumps(data)}
    )

    assert response.status_code == 200
    assert response.json() == {
        'status': 'Check your email for confirmation letter.'
    }

    token = JWT.create_token({'name': data['name']}, exp_time=360)
    response = await c.get(f'/enterprises/register-confirm/{token}')
    assert response.status_code == 201
    assert response.json() == {
        'status': 'Enterprise has been created successfully'
    }


@pytest.mark.parametrize('path, status, res', [
    ('/enterprises/', 200, []),
    ('/enterprises/admin', 200, []),
    ('/enterprises/admin/services', 200, []),
])
async def test_get_user_routers(c, path, status, res):
    response = await c.get(path)
    assert response.status_code == status
    if path == '/enterprises/':
        assert response.json() != res
    if path == '/enterprises/admin':
        assert response.json()['name'] == 'admin'
    if path == '/enterprises/admin/services':
        assert response.json() == res


async def test_update_enterprise(aec):
    response = await aec.patch('/enterprises/me', data={'name': 'lmao'})
    assert response.status_code == 202

    # update the Authorization header with the new username
    token = aec.headers['Authorization'].split()[1]
    response = await aec.post(
        url='/auth/token/refresh',
        json={'refresh_token': token, 'enterprise': 'lmao'}
    )
    assert response.status_code == 200
    new_token = 'Bearer ' + response.json()['access_token']
    aec.headers.update({'Authorization': new_token})

    response = await aec.get('/enterprises/lmao')
    assert response.status_code == 200


async def test_delete_enterprise(aec):
    response = await aec.delete('/enterprises/me')
    assert response.status_code == 204

    response = await aec.get('/enterprises/lmao')
    assert response.status_code == 404
