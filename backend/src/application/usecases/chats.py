from src.application.dtos.chats import ChatSchema
from src.application.interfaces.services.tokens import ITokenService
from src.application.interfaces.repositories.users import IUserRepository
from src.application.interfaces.repositories.chats import IChatRepository


class ChatUseCase:

    def __init__(
        self,
        chat_repo: IChatRepository,
        user_repo: IUserRepository,
        token_service: ITokenService,
    ):
        self.chat_repo = chat_repo
        self.user_repo = user_repo
        self.token_service = token_service

    async def create_chat(self, first_user_id: int, second_user_id: int):
        data = {'first_user_id': first_user_id, 'second_user_id': second_user_id}
        async with self.chat_repo.uow:
            chat = await self.chat_repo.add(data)
        return ChatSchema(**chat.to_dict())

    async def get_chats(self, user_id: int) -> list:
        return await self.chat_repo.get_chats(user_id)

    async def get_chat(self, user_id: int, chat_id: int):
        chat = await self.chat_repo.retrieve(chat_id=chat_id, user_id=user_id)
        return ChatSchema(**chat.to_dict())

    async def get_chat_id(self, first_user_id: int, second_user_id: int):
        chat_id = await self.chat_repo.get_chat_id(first_user_id, second_user_id)
        return chat_id

    async def get_chat_messages(self, chat_id: int):
        return await self.chat_repo.get_chat_messages(chat_id)

    async def get_sender_id(self, token: str):
        token_data = await self.token_service.decode(token)
        user_id = token_data.get('id')
        return user_id

    async def get_connection_manager(self):
        return await ConnectionManager(self.chat_repo, self.user_repo)


class ConnectionManager:

    def __init__(
        self,
        chat_repo: IChatRepository,
        user_repo: IUserRepository,
    ):
        self.active_connections: dict[int, list] = {}
        self.chat_repo = chat_repo
        self.user_repo = user_repo

    async def connect(self, websocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        
        self.active_connections[chat_id].append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket, chat_id: int):
        self.active_connections[chat_id].remove(websocket)
        print(self.active_connections)

    async def send_message(self, data: dict):
        content = data['content']
        chat_id = data['chat_id']
        sender_id = data['sender_id']
        msg_id = await self.save_to_db(chat_id, sender_id, content)
        
        user = self.user_repo.retrieve(id=sender_id)
        data['id'] = msg_id
        data['sender'] = {}
        data['sender']['username'] = user.username
        data['sender']['avatar'] = user.avatar
        
        for connection in self.active_connections[chat_id]:
            await connection.send_json(data)

    async def receive_message(self, websocket):
        data = await websocket.receive_json()
        return data

    async def save_to_db(self, chat_id: int, sender_id: int, content: str):
        data = {'chat_id': chat_id, 'sender_id': sender_id, 'content': content}
        async with self.chat_repo.uow:       
            return await self.chat_repo.add_message(data)
