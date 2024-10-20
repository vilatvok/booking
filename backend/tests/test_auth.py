from unittest.mock import patch

from src.utils.tokens import JWT


@patch('src.celery.send_password_reset.apply_async')
async def test_password_reset(mock_send_password_reset, c):
    mock_send_password_reset.return_value = None

    # test user password reset
    user_data = {
        'model': 'user',
        'email': 'john@gmail.com',
    }
    response1 = await c.post(
        url='/auth/password-reset',
        json=user_data,
    )
    assert response1.status_code == 202, response1.json()

    # test enterprise password reset
    enterprise_data = {
        'model': 'enterprise',
        'email': 'john@gmail.com',
    }
    response2 = await c.post(
        url='/auth/password-reset',
        json=enterprise_data,
    )
    assert response2.status_code == 202, response2.json()


async def test_password_reset_confirm(c):
    form_data = {
        'password1': '12345rtx',
        'password2': '12345rtx',
    }

    # test user password reset
    data = {
        'model': 'user',
        'email': 'john@gmail.com',
    }
    token = JWT.create_token(data)

    response1 = await c.patch(f'/auth/password-reset/{token}', json=form_data)
    assert response1.status_code == 200, response1.json()

    # test enterprise password reset
    data = {
        'model': 'enterprise',
        'email': 'john@gmail.com'
    }
    token = JWT.create_token(data)
    response2 = await c.patch(f'/auth/password-reset/{token}', json=form_data)
    assert response2.status_code == 200, response2.json()
