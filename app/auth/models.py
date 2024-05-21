import uuid

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    avatar = sa.Column(sa.String, default='app/static/images/user_logo.png')
    email = sa.Column(sa.String)
    service = relationship(
        'Service',
        back_populates='owner',
        cascade='all, delete-orphan',
    )
    feedbacks = relationship(
        'Feedback',
        back_populates='user',
        cascade='all, delete-orphan',
    )


class Enterprise(Base):
    __tablename__ = 'enterprise'

    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String, unique=True, nullable=False)
    owner = sa.Column(sa.String, nullable=False)
    logo = sa.Column(sa.String, default='app/static/images/company_logo.png')
    password = sa.Column(sa.String, nullable=False)
    created = sa.Column(sa.Date, nullable=False)
    is_verified = sa.Column(sa.Boolean, default=False)
