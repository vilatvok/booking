import factory

from src.infrastructure.models.chats import Chat, Message
from tests.factories.users import AsyncFactory


class ChatFactory(AsyncFactory):
    class Meta:
        model = Chat

    first_user_id = 1
    second_user_id = 1


class MessageFactory(AsyncFactory):
    class Meta:
        model = Message

    chat_id = 1
    sender_id = 1
    content = factory.Faker('sentence')
