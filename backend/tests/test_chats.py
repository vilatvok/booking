
async def test_create_chat(ac):
    response = await ac.post('/chats/', json={'user_id': 2})
    assert response.status_code == 201


async def test_get_chats(ac):
    response = await ac.get('/chats/')
    assert response.status_code == 200


async def test_get_chat(ac):
    response = await ac.get('/chats/1')
    assert response.status_code == 200


async def test_get_chat_id(ac):
    response = await ac.get('/chats/id', params={'user_id': 2})
    assert response.status_code == 200


async def test_get_chat_messages(ac):
    response = await ac.get('/chats/1/messages')
    assert response.status_code == 200
