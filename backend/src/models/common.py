from typing import TYPE_CHECKING, Annotated
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, mapped_column

# import models only in case type checking
# # when: Mapped[list['Feedback']]
if TYPE_CHECKING:
    from src.models.services import Service
    from src.models.chats import Chat, Message


class Base(DeclarativeBase):
    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]


class Owner(Base):
    __tablename__ = 'owner'

    discriminator: Mapped[str]
    services: Mapped[list['Service']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )
    chats: Mapped[list['Chat']] = relationship(
        primaryjoin="or_(Chat.first_user_id == Owner.id, Chat.second_user_id == Owner.id)",
        viewonly=True,
    )
    messages: Mapped[list['Message']] = relationship(
        back_populates='sender',
        viewonly=True,
    )
    
    __mapper_args__ = {
        'polymorphic_identity': 'owner',
        'polymorphic_on': 'discriminator'
    }
