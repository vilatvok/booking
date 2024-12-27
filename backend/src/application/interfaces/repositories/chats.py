from abc import abstractmethod

from src.application.interfaces.repositories.base import ISqlRepository


class IChatRepository(ISqlRepository):

    @abstractmethod
    async def get_chats(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_chat_id(self, first_user_id: int, second_user_id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_chat_messages(self, chat_id: int):
        raise NotImplementedError

    @abstractmethod
    async def add_message(self, data: dict):
        raise NotImplementedError
