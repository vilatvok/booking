from datetime import datetime
from sqlalchemy import ForeignKey, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities import chats as entities
from src.infrastructure.models.base import Base
from src.infrastructure.models.users import User


class Chat(Base):
    __tablename__ = 'chat'
    __table_args__ = (
        CheckConstraint('first_user_id != second_user_id'),
    )

    first_user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    second_user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )

    first_user: Mapped['User'] = relationship(
        back_populates='chats',
        foreign_keys=[first_user_id]
    )
    second_user: Mapped['User'] = relationship(
        back_populates='chats',
        foreign_keys=[second_user_id]
    )
    messages: Mapped[list['Message']] = relationship(back_populates='chat')

    def to_entity(self):
        return entities.Chat(
            id=self.id,
            first_user_id=self.first_user_id,
            second_user_id=self.second_user_id
        )


class Message(Base):
    __tablename__ = 'message'

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('chat.id', ondelete='CASCADE')
    )
    sender_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    content: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    chat: Mapped['Chat'] = relationship(back_populates='messages')
    sender: Mapped['User'] = relationship(back_populates='messages')

    def to_entity(self):
        return entities.Message(
            id=self.id,
            chat_id=self.chat_id,
            sender_id=self.sender_id,
            content=self.content,
            timestamp=self.timestamp
        )
