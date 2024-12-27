from typing import Annotated
from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect

from src.application.usecases.chats import ConnectionManager
from src.application.dtos.users import UserComplete
from src.application.dtos.chats import ChatSchema
from src.presentation.api.dependencies.users import current_user
from src.presentation.api.dependencies.usecases import chat_usecase


router = APIRouter()


@router.post("/", status_code=201, response_model=ChatSchema)
async def create_chat(
    current_user: Annotated[UserComplete, current_user],
    chat_usecase: chat_usecase,
    user_id: Annotated[int, Body(embed=True)],
):
    return await chat_usecase.create_chat(current_user.id, user_id)



@router.get("/", response_model=list[ChatSchema])
async def get_chats(
    current_user: Annotated[UserComplete, current_user],
    chat_usecase: chat_usecase,
):
    return await chat_usecase.get_chats(current_user.id)


@router.get("/id")
async def get_chat_id(
    user_id: int,
    current_user: Annotated[UserComplete, current_user],
    chat_usecase: chat_usecase,
):
    return await chat_usecase.get_chat_id(current_user.id, user_id)


@router.get("/{chat_id}", response_model=ChatSchema)
async def get_chat(
    chat_id: int,
    current_user: Annotated[UserComplete, current_user],
    chat_usecase: chat_usecase,
):
    return await chat_usecase.get_chat(current_user.id, chat_id)


@router.get("/{chat_id}/messages", dependencies=[current_user])
async def get_chat_messages(chat_id: int, chat_usecase: chat_usecase):
    return await chat_usecase.get_chat_messages(chat_id)



@router.websocket("/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    token: str,
    chat_usecase: chat_usecase,
) -> None:
    sender_id = await chat_usecase.get_sender_id(token)
    manager: ConnectionManager = chat_usecase.get_connection_manager()
    
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await manager.receive_message(websocket)
            msg_data = {
                'chat_id': chat_id,
                'sender_id': sender_id,
                'content': data['content'],
            }
            await manager.send_message(msg_data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
