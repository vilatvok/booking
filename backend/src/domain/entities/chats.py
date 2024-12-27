from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.base import Entity


@dataclass
class Chat(Entity):
    first_user_id: int
    second_user_id: int


@dataclass
class Message(Entity):
    chat_id: int
    sender_id: int
    content: str
    timestamp: datetime
