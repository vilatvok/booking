from typing import Annotated
from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect
from sqlalchemy import insert, select, or_, and_
from sqlalchemy.orm import joinedload

from src.exceptions import not_found
from src.dependencies import db_session, current_user
from src.schemas.users import UserSchema
from src.schemas.enterprises import EnterpriseSchema
from src.schemas.chats import ChatID, ChatSchema
from src.models.chats import Chat
from src.models.users import User
from src.utils.tokens import JWT
from src.utils.chats import manager


router = APIRouter()


@router.get("/", response_model=list[ChatSchema])
async def get_chats(
    db: db_session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
):
    user_id = current_user.id
    query = (
        select(Chat).
        where(
            or_(
                (Chat.first_user_id == user_id),
                (Chat.second_user_id == user_id)
            )
        )
    )
    chats = await db.execute(query)
    return chats.scalars().all()


@router.post("/id")
async def get_chat_id(
    db: db_session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    form: ChatID,
):
    first_user_id = current_user.id
    second_user_id = form.obj_id
    query = (
        select(Chat).
        where(
            or_(
                and_(
                    (Chat.first_user_id == first_user_id),
                    (Chat.second_user_id == second_user_id)
                ),
                and_(
                    (Chat.first_user_id == second_user_id),
                    (Chat.second_user_id == first_user_id)
                )
            )
        )
    )
    chat = (await db.execute(query)).scalar()
    if not chat:
        raise not_found
    return chat.id


@router.get("/{chat_id}", response_model=ChatSchema)
async def get_chat(
    db: db_session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    chat_id: int,
):
    user_id = current_user.id
    query = (
        select(Chat).
        where(
            and_(
                (Chat.id == chat_id),
                (or_(
                    (Chat.first_user_id == user_id),
                    (Chat.second_user_id == user_id)
                ))
            )
        )
    )
    chat = (await db.execute(query)).scalar()
    if not chat:
        raise not_found
    return chat


@router.get("/{chat_id}/messages")
async def get_chat_messages(db: db_session, chat_id: int):
    query = (
        select(Chat).
        options(joinedload(Chat.messages)).
        where(Chat.id == chat_id)
    )
    chat = (await db.execute(query)).scalar()
    if not chat:
        raise not_found
    return chat.messages


@router.post("/", status_code=201)
async def create_chat(
    db: db_session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    user_id: Annotated[int, Body(embed=True)],
):
    first_user_id = current_user.id
    second_user_id = user_id
    stmt = (
        insert(Chat).
        values(first_user_id=first_user_id, second_user_id=second_user_id).
        returning(Chat.id)
    )
    obj = (await db.execute(stmt)).scalar()
    await db.commit()
    return obj


@router.websocket("/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    db: db_session,
    chat_id: int,
    token: str,
) -> None:
    token_data = JWT.decode_token(token)
    username = token_data.get('name')
    user = (await db.execute(
        select(User).
        where(User.username == username))
    ).scalar()
    await manager.connect(websocket)
    try:
        while True:
            data = await manager.receive_message(websocket)
            msg_data = {
                'chat_id': chat_id,
                'sender_id': user.id,
                'content': data,
            }
            await manager.send_message(msg_data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
