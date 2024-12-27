from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.base import Entity


@dataclass
class User(Entity):
    username: str
    password: str
    email: str | None = None
    is_active: bool = False
    is_company: bool = False
    social_id: str | None = None
    avatar: str = 'static/img/user_logo.png'
    provider: str = 'local'


@dataclass
class Company(Entity):
    user_id: int
    owner: str
    email: str
    name: str
    created_at: datetime
    logo: str = 'static/img/company_logo.png'
