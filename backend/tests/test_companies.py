import json

from tests.factories.users import CompanyFactory


async def test_registration(c):
    input_data = {
        'name': 'test_company',
        'owner': 'Test owner',
        'email': 'foo@gmail.com',
        'password': '12345rtx'
    }

    response = await c.post(
        url='/companies/register',
        data={'form_data': json.dumps(input_data)}
    )

    assert response.status_code == 200


async def test_get_companies(c):
    response = await c.get('/companies/')
    assert response.status_code == 200
    assert response.json() != []


async def test_get_company(c):
    obj = await CompanyFactory()
    response = await c.get(f'/companies/{obj.name}')
    assert response.status_code == 200


async def test_get_company_offers(c):
    obj = await CompanyFactory()
    response = await c.get(f'/companies/{obj.name}/offers')
    assert response.status_code == 200


async def test_update_company(ac):
    response = await ac.patch('/companies/me', data={'name': 'lmao'})
    assert response.status_code == 202

    # update the Authorization header with the new name
    token = ac.headers['Authorization'].split()[1]
    response = await ac.post(
        url='/auth/token/refresh',
        json={'refresh_token': token, 'company': 'lmao'}
    )
    assert response.status_code == 200
    new_token = 'Bearer ' + response.json()['access_token']
    ac.headers.update({'Authorization': new_token})

    response = await ac.get('/companies/lmao')
    assert response.status_code == 200


async def test_delete_companies(ac):
    response = await ac.delete('/companies/me')
    assert response.status_code == 204

    response = await ac.get('/companies/lmao')
    assert response.status_code == 404
