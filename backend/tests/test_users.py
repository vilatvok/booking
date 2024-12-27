import json

from unittest.mock import patch

from src.infrastructure.services.tokens import JWTService
from tests.factories.users import UserFactory


@patch('fastapi.background.BackgroundTasks.add_task', return_value=None)
@patch('src.presentation.api.routers.users.scheduler.add_job', return_value=None)
async def test_registration(mock_send_confirmation_letter, mock_scheduler, c):
    input_data = {
        'username': 'test_user',
        'email': 'foo@gmail.com',
        'password': '12345tkr',
    }

    # test registration router
    response = await c.post(
        url='/auth/register',
        data={'form_data': json.dumps(input_data)}
    )
    assert response.status_code == 200

    # create fake token for confirmation
    created_user = await UserFactory(username=input_data['username'])
    token_data = {'obj_id': created_user.id, 'email': input_data['email']}
    token = JWTService.encode(token_data, exp_time=360)

    # test confirmation router
    response = await c.get(f'/auth/register-confirm/{token}')
    assert response.status_code == 201


async def test_get_users(c):
    response = await c.get('/users/')
    assert response.status_code == 200
    assert response.json() != []


async def test_get_user(c):
    user = await UserFactory()
    response = await c.get(f'/users/{user.username}')
    assert response.status_code == 200


async def test_get_user_offers(c):
    user = await UserFactory()
    response = await c.get(f'/users/{user.username}/offers')
    assert response.status_code == 200


async def test_update_user(ac):
    response = await ac.patch('/users/me', data={'username': 'lmao'})
    assert response.status_code == 202

    # update the Authorization header with the new username
    token = ac.headers['Authorization'].split()[1]
    response = await ac.post(
        url='/auth/token/refresh',
        json={'refresh_token': token, 'username': 'lmao'}
    )
    assert response.status_code == 200
    new_token = 'Bearer ' + response.json()['access_token']
    ac.headers.update({'Authorization': new_token})

    response = await ac.get('/users/lmao')
    assert response.status_code == 200


async def test_delete_user(ac):
    response = await ac.delete('/users/me')
    assert response.status_code == 204

    response = await ac.get('/users/admin')
    assert response.status_code == 404


@patch('fastapi.background.BackgroundTasks.add_task', return_value=None)
async def test_password_reset(mocked_task, c):
    user = await UserFactory(username='admin')
    user_data = {'email': user.email}

    user_response = await c.post('/users/password-reset', json=user_data)
    assert user_response.status_code == 202, user_response.json()


async def test_password_reset_confirm(c):
    user = await UserFactory(username='admin')

    form_data = {'password1': '12345rtx', 'password2': '12345rtx'}
    token_data = {
        'email': user.email,
        'user_id': user.id,
    }

    token = JWTService.encode(token_data)
    response = await c.patch(f'/users/password-reset/{token}', json=form_data)
    assert response.status_code == 200, response.json()


async def test_change_password(ac):
    password_data = {
        'old_password': 'ybdaa0tit',
        'new_password': '12345tkr',
    }

    response = await ac.put('/users/password', json=password_data)
    assert response.status_code == 202, response.json()


async def test_logout(ac):
    response = await ac.post('/users/auth')

    assert response.status_code == 200, response.json()
    assert response.json() == {'status': 'You logged out'}
