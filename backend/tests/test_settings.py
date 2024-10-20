
async def test_change_user_password(c, auc):
    response = await auc.put(
        url='/settings/password',
        json={
            'old_password': '12345rtx',
            'new_password': '12345tkr',
        }
    )

    assert response.status_code == 202, response.json()
    assert response.json() == {'status': 'changed'}

    response = await c.post(url='/users/login', data={
        'username': 'admin',
        'password': '12345tkr',
    })
    assert response.status_code == 200, response.json()


async def test_change_enterprise_password(c, aec):
    response = await aec.put(
        url='/settings/password',
        json={
            'old_password': '12345rtx',
            'new_password': '12345tkr',
        }
    )

    assert response.status_code == 202, response.json()
    assert response.json() == {'status': 'changed'}

    response = await c.post(url='/enterprises/login', data={
        'username': 'john@gmail.com',
        'password': '12345tkr',
    })
    assert response.status_code == 200, response.json()


async def test_logout(auc):
    response = await auc.post('/settings/logout')

    assert response.status_code == 200, response.json()
    assert response.json() == {'status': 'You logged out'}
