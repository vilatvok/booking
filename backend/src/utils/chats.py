from fastapi import WebSocket
from sqlalchemy import insert

from src.database import session_manager
from src.models.chats import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(
        self,
        data: dict,
        websocket: WebSocket,
    ):  
        chat_id = data['chat_id']
        sender_id = data['sender_id']
        content = data['content']
        msg_id = await self.save_to_db(chat_id, sender_id, content)
        
        # Add message id to the data
        data['id'] = msg_id
        await websocket.send_json(data)

    async def receive_message(self, websocket: WebSocket):
        data = await websocket.receive_json()
        return data

    @staticmethod
    async def save_to_db(chat_id: int, sender_id: int, content: str) -> int:
        async with session_manager.session() as session:
            stmt = (
                insert(Message).
                values(
                    chat_id=chat_id,
                    sender_id=sender_id,
                    content=content,
                ).returning(Message.id)
            )
            msg_id = await session.execute(stmt)
            await session.commit()
        return msg_id.scalar()


manager = ConnectionManager()
