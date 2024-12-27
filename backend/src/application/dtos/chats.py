from pydantic import BaseModel


class ChatSchema(BaseModel):
    id: int
    first_user_id: int
    second_user_id: int

