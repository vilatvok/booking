import sqlalchemy as sa

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base
from app.auth.models import User
from app.service.schemas import ServiceType, Rate, IntEnum


class Service(Base):
    __tablename__ = 'service'

    id = sa.Column(sa.Integer, primary_key=True)
    owner_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id, ondelete='CASCADE'),
    )
    owner = relationship('User', back_populates='service')
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    type = sa.Column(sa.Enum(ServiceType), nullable=False)
    city = sa.Column(sa.String, nullable=False)
    phone = sa.Column(sa.String, nullable=False)
    images = relationship(
        'Image',
        back_populates='service',
        cascade='all, delete-orphan',
    )
    prices = relationship(
        'Prices',
        back_populates='service',
        cascade='all, delete-orphan',
    )
    feedbacks = relationship(
        'Feedback',
        back_populates='service',
        cascade='all, delete-orphan',
    )


class Image(Base):
    __tablename__ = 'image'

    id = sa.Column(sa.Integer, primary_key=True)
    service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Service.id, ondelete='CASCADE'),
    )
    data = sa.Column(sa.String, nullable=False)
    service = relationship('Service', back_populates='images')


class Prices(Base):
    __tablename__ = 'prices'

    id = sa.Column(sa.Integer, primary_key=True)
    service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Service.id, ondelete='CASCADE'),
    )
    service = relationship('Service', back_populates='prices')
    per_hour = sa.Column(sa.Float)
    per_day = sa.Column(sa.Float)
    per_month = sa.Column(sa.Float)
    per_year = sa.Column(sa.Float)


class Feedback(Base):
    __tablename__ = 'feedback'

    id = sa.Column(sa.Integer, primary_key=True)
    service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Service.id, ondelete='CASCADE'),
    )
    service = relationship('Service', back_populates='feedbacks')
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(User.id, ondelete='CASCADE'),
        unique=True,
    )
    user = relationship('User', back_populates='feedbacks')
    text = sa.Column(sa.Text, nullable=False)
    rating = sa.Column(IntEnum(Rate), nullable=False)
    created = sa.Column(sa.DateTime, default=datetime.utcnow)
