from datetime import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.common import Owner


class Enterprise(Owner):
    __tablename__ = 'enterprise'

    id: Mapped[int] = mapped_column(ForeignKey('owner.id'), primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    logo: Mapped[str] = mapped_column(default='static/images/company_logo.png')
    owner: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    is_active: Mapped[bool] = mapped_column(default=False)

    __mapper_args__ = {'polymorphic_identity': 'enterprise'}
