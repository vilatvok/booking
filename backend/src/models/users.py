from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.common import Owner
# import models only in case type checking
# when: Mapped[list['Feedback']]
if TYPE_CHECKING:
    from src.models.services import Feedback


class User(Owner):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(ForeignKey('owner.id'), primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    avatar: Mapped[str] = mapped_column(default='static/images/user_logo.png')
    email: Mapped[str | None] = mapped_column(unique=True)
    password: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=False)
    social_id: Mapped[str | None] = mapped_column(unique=True)
    provider: Mapped[str] = mapped_column(default='local')

    feedbacks: Mapped[list['Feedback']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    __mapper_args__ = {'polymorphic_identity': 'user'}
