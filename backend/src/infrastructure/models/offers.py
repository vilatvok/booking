from datetime import datetime
from sqlalchemy import ForeignKey, SmallInteger, CheckConstraint, UniqueConstraint, text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.domain.entities import offers as entities
from src.infrastructure.models.base import Base
from src.infrastructure.models.users import User


class Offer(Base):
    __tablename__ = 'offer'

    # Columns
    name: Mapped[str]
    description: Mapped[str]
    offer_type: Mapped[entities.OfferType]
    phone: Mapped[str]
    city: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    # Foreign keys
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )

    # Relationships
    owner: Mapped['User'] = relationship(back_populates='offers')
    images: Mapped[list['Image']] = relationship(back_populates='offer')
    prices: Mapped['Price'] = relationship(back_populates='offer')
    feedbacks: Mapped[list['Feedback']] = relationship(back_populates='offer')

    def to_entity(self):
        return entities.Offer(
            id=self.id,
            name=self.name,
            description=self.description,
            offer_type=self.offer_type,
            city=self.city,
            phone=self.phone,
            created_at=self.created_at,
            owner_id=self.owner_id,
        )


class Image(Base):
    __tablename__ = 'image'

    # Columns
    data: Mapped[str]

    # Foreign keys
    offer: Mapped['Offer'] = relationship(back_populates='images')
    offer_id: Mapped[int] = mapped_column(
        ForeignKey('offer.id', ondelete='CASCADE'),
    )

    def to_entity(self):
        return entities.Image(
            id=self.id,
            offer_id=self.offer_id,
            data=self.data,
        )


class Price(Base):
    __tablename__ = 'price'

    per_hour: Mapped[float] = mapped_column(
        CheckConstraint('per_hour >= 0', name='check_per_hour_positive'),
    )
    per_day: Mapped[float] = mapped_column(
        CheckConstraint('per_day >= 0', name='check_per_day_positive'),
    )
    per_month: Mapped[float] = mapped_column(
        CheckConstraint('per_month >= 0', name='check_per_month_positive'),
    )
    per_year: Mapped[float] = mapped_column(
        CheckConstraint('per_year >= 0', name='check_per_year_positive'),
    )

    # Foreign keys
    offer: Mapped['Offer'] = relationship(back_populates='prices')
    offer_id: Mapped[int] = mapped_column(
        ForeignKey('offer.id', ondelete='CASCADE'),
    )

    def to_entity(self):
        return entities.Price(
            id=self.id,
            offer_id=self.offer_id,
            per_hour=self.per_hour,
            per_day=self.per_day,
            per_month=self.per_month,
            per_year=self.per_year,
        )


class Feedback(Base):
    __tablename__ = 'feedback'
    __table_args__ = (
        UniqueConstraint('user_id', 'offer_id', name='unique_user_offer_feedback'),
    )

    # Columns
    text: Mapped[str]
    rating: Mapped[int] = mapped_column(
        SmallInteger,
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating'),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    offer_id: Mapped[int] = mapped_column(
        ForeignKey('offer.id', ondelete='CASCADE'),
    )

    # Relationships
    user: Mapped['User'] = relationship(back_populates='feedbacks')
    offer: Mapped['Offer'] = relationship(back_populates='feedbacks')

    def to_entity(self):
        return entities.Feedback(
            id=self.id,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
            user_id=self.user_id,
            offer_id=self.offer_id,
        )
