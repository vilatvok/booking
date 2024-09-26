from datetime import datetime

from sqlalchemy import ForeignKey, SmallInteger, CheckConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.common import Base
from src.schemas.services import ServiceType
from src.models.common import Owner
from src.models.users import User


class Service(Base):
    __tablename__ = 'service'

    name: Mapped[str]
    description: Mapped[str]
    type: Mapped[ServiceType]
    phone: Mapped[str]
    city: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey('owner.id', ondelete='CASCADE'),
    )
    owner: Mapped['Owner'] = relationship(back_populates='services')

    images: Mapped[list['Image']] = relationship(
        back_populates='service',
        cascade='all, delete-orphan',
    )
    prices: Mapped['Price'] = relationship(
        back_populates='service',
        cascade='all, delete-orphan',
    )
    feedbacks: Mapped[list['Feedback']] = relationship(
        back_populates='service',
        cascade='all, delete-orphan',
    )


class Image(Base):
    __tablename__ = 'image'

    data: Mapped[str]

    service: Mapped['Service'] = relationship(back_populates='images')
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id', ondelete='CASCADE'),
    )


class Price(Base):
    __tablename__ = 'price'

    per_hour: Mapped[float]
    per_day: Mapped[float]
    per_month: Mapped[float]
    per_year: Mapped[float]

    service: Mapped['Service'] = relationship(back_populates='prices')
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id', ondelete='CASCADE'),
    )


class Feedback(Base):
    __tablename__ = 'feedback'

    text: Mapped[str]
    rating: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating'),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    user: Mapped['User'] = relationship(back_populates='feedbacks')
    service: Mapped['Service'] = relationship(back_populates='feedbacks')
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id', ondelete='CASCADE'),
    )
