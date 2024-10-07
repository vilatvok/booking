from fastapi import APIRouter, Depends

from src.schemas.tokens import Token, RefreshToken
from src.dependencies import get_redis_session
from src.utils.tokens import JWT


router = APIRouter()


@router.post('/token/refresh', response_model=Token)
async def update_token(form: RefreshToken, rdb = Depends(get_redis_session)):
    refresh_token = form.refresh_token
    data = {}
    if form.username:
        data['username'] = form.username 
    elif form.enterprise:
        data['enterprise'] = form.enterprise

    if not data:
        data = JWT.decode_token(refresh_token, rdb=rdb)
        access = JWT.create_token(data)
        return Token(access_token=access)
    else:
        access = JWT.create_token(data)
        refresh = JWT.create_token(data, exp_time=1440)
        return Token(access_token=access, refresh_token=refresh)
