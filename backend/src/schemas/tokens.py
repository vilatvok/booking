from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str


class RefreshToken(BaseModel):
    refresh: str
    username: str | None = None