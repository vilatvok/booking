from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.services.schemas import ServiceType, Rate
from src.utils import pk, created_at
from src.auth.models import User


class Service(Base):
    __tablename__ = 'service'

    id: Mapped[pk]
    name: Mapped[str]
    description: Mapped[str]
    type: Mapped[ServiceType]
    phone: Mapped[str]
    created_at: Mapped[created_at]

    owner: Mapped['User'] = relationship(back_populates='service')
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    images: Mapped[list['Image']] = relationship(
        back_populates='service',
        cascade='all, delete-orphan',
    )
    prices: Mapped[list['Price']] = relationship(
        back_populates='service',
        cascade='all, delete-orphan',
    )
    feedbacks: Mapped[list['Feedback']] = relationship(
        back_populates='service',
        cascade='all, delete-orphan',
    )


class Image(Base):
    __tablename__ = 'image'

    id: Mapped[pk]
    data: Mapped[str]

    service: Mapped['Service'] = relationship(back_populates='images')
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id', ondelete='CASCADE'),
    )


class Price(Base):
    __tablename__ = 'price'

    id: Mapped[pk]
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

    id: Mapped[pk]
    text: Mapped[str]
    rating: Mapped[Rate]
    created_at: Mapped[created_at]

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    user: Mapped['User'] = relationship(back_populates='feedbacks')
    service: Mapped['Service'] = relationship(back_populates='feedbacks')
    service_id: Mapped[int] = mapped_column(
        ForeignKey('service.id', ondelete='CASCADE'),
    )
