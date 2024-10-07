from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None


class RefreshToken(BaseModel):
    refresh_token: str
    username: str | None = None
    enterprise: str | None = None

