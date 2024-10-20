from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text

from src.models.common import Base, Owner


class Chat(Base):
    __tablename__ = 'chat'

    first_user_id: Mapped[int] = mapped_column(
        ForeignKey('owner.id', ondelete='CASCADE')
    )
    second_user_id: Mapped[int] = mapped_column(
        ForeignKey('owner.id', ondelete='CASCADE')
    )

    first_user: Mapped['Owner'] = relationship(
        back_populates='chats',
        foreign_keys=[first_user_id]
    )
    second_user: Mapped['Owner'] = relationship(
        back_populates='chats',
        foreign_keys=[second_user_id]
    )
    messages: Mapped[list['Message']] = relationship(
        back_populates='chat',
        cascade='all, delete-orphan',
    )


class Message(Base):
    __tablename__ = 'message'

    chat_id: Mapped[int] = mapped_column(
        ForeignKey('chat.id', ondelete='CASCADE')
    )
    sender_id: Mapped[int] = mapped_column(
        ForeignKey('owner.id', ondelete='CASCADE')
    )
    content: Mapped[str] = mapped_column()
    timestamp: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    chat: Mapped['Chat'] = relationship(back_populates='messages')
    sender: Mapped['Owner'] = relationship(back_populates='messages')
