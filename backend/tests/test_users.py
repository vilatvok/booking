import json
import pytest

from unittest.mock import patch

from src.utils.tokens import JWT


@patch('src.celery.send_confirmation_letter.apply_async')
async def test_registration(mock_send_confirmation_letter, c):
    mock_send_confirmation_letter.return_value = None
    # test data
    data = {
        'username': 'asasa',
        'email': 'foo@gmail.com',
        'password': '12345tkr',
    }

    # test registration router
    response = await c.post(
        url='/users/register',
        data={'form': json.dumps(data)}
    )
    assert response.status_code == 200
    assert response.json() == {
        'status': 'Check your email for confirmation letter.'
    }

    # create fake token for confirmation
    token = JWT.create_token({'name': data['username']}, exp_time=360)

    # test confirmation router
    response = await c.get(f'/users/register-confirm/{token}')
    assert response.status_code == 201
    assert response.json() == {
        'status': 'User has been created successfully'
    }


@pytest.mark.parametrize('path, status, res', [
    ('/users/', 200, []),
    ('/users/admin', 200, 'admin'),
    ('/users/admin/services', 200, []),
])
async def test_get_user_routers(c, path, status, res):
    response = await c.get(path)
    assert response.status_code == status
    match path:
        case '/users/':
            assert response.json() != res
        case '/users/admin':
            assert response.json()['username'] == res
        case '/users/admin/services':
            assert response.json() == res


async def test_update_user(auc):
    response = await auc.patch('/users/me', data={'username': 'lmao'})
    assert response.status_code == 202

    # update the Authorization header with the new username
    token = auc.headers['Authorization'].split()[1]
    response = await auc.post(
        url='/auth/token/refresh',
        json={'refresh_token': token, 'username': 'lmao'}
    )
    assert response.status_code == 200
    new_token = 'Bearer ' + response.json()['access_token']
    auc.headers.update({'Authorization': new_token})

    response = await auc.get('/users/lmao')
    assert response.status_code == 200


async def test_delete_user(auc):
    response = await auc.delete('/users/me')
    assert response.status_code == 204

    response = await auc.get('/users/admin')
    assert response.status_code == 404
