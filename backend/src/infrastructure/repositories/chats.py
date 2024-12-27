from sqlalchemy import select, or_, and_
from sqlalchemy.orm import joinedload

from src.application.interfaces.repositories.chats import IChatRepository
from src.infrastructure.repositories.base import SQLAlchemyRepository, switch_model
from src.infrastructure.models.chats import Chat, Message
from src.infrastructure.models.users import User, Company


class ChatRepository(SQLAlchemyRepository, IChatRepository):
    model = Chat

    @switch_model(Message)
    async def add_message(self, data: dict):
        return await self.add(data)

    async def retrieve(self, **kwargs):
        user_id = kwargs.get('user_id')
        query = (
            select(self.model).
            where(
                and_(
                    (self.model.id == kwargs.get('chat_id')),
                    (or_(
                        (self.model.first_user_id == user_id),
                        (self.model.second_user_id == user_id)
                    ))
                )
            )
        )
        return await self.get_scalar(query)

    async def get_chats(self, user_id: int):
        query = (
            select(self.model).
            where(
                or_(
                    (self.model.first_user_id == user_id),
                    (self.model.second_user_id == user_id)
                )
            )
        )
        chats = await self.session.execute(query)
        return chats.scalars().all()

    async def get_chat_id(self, first_user_id: int, second_user_id: int):
        query = (
            select(self.model.id).
            where(
                or_(
                    and_(
                        (self.model.first_user_id == first_user_id),
                        (self.model.second_user_id == second_user_id)
                    ),
                    and_(
                        (self.model.first_user_id == second_user_id),
                        (self.model.second_user_id == first_user_id)
                    )
                )
            )
        )
        return await self.get_scalar(query)

    @switch_model(Message)
    async def get_chat_messages(self, chat_id: int):
        query = (
            select(self.model).
            options(
                joinedload(self.model.sender).
                selectin_polymorphic([User, Company])
            ).
            where(self.model.chat_id == chat_id)
        )
        messages = await self.session.execute(query)
        return messages.scalars().all()
