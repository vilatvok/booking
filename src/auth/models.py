import uuid

from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.utils import pk, created_at

from typing import TYPE_CHECKING


# import models only in case type checking
# when: Mapped[list['Feedback']]
if TYPE_CHECKING:
    from src.services.models import Service, Feedback


class User(Base):
    __tablename__ = 'users'

    id: Mapped[pk]
    username: Mapped[str] = mapped_column(unique=True)
    avatar: Mapped[str] = mapped_column(default='src/static/images/user_logo.png')
    email: Mapped[str | None]
    password: Mapped[str]

    service: Mapped[list['Service']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )
    feedbacks: Mapped[list['Feedback']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )


class Enterprise(Base):
    __tablename__ = 'enterprise'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True)
    logo: Mapped[str] = mapped_column(default='src/static/images/company_logo.png')
    owner: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[created_at]
