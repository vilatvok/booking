import requests

from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.datastructures import UploadFile
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError

from src.utils.tokens import JWT
from src.utils.common import generate_image_path
from src.models.users import User
from src.dependencies import anonymous_user, session
from src.schemas.tokens import Token
from src.schemas.users import UserSocialRegister
from src.config import Settings, get_settings


router = APIRouter()


@router.get('/signin', dependencies=[anonymous_user])
async def login_google(settings: Annotated[Settings, Depends(get_settings)]):
    url = 'https://accounts.google.com/o/oauth2/auth'
    client_id = f'client_id={settings.google_client_id}'
    redirect_uri = f'redirect_uri={settings.google_redirect_uri}'
    response_type = 'response_type=code'
    scope = 'scope=openid%20profile%20email'
    access_type = 'access_type=offline'

    return {
        'url': f'{url}?{response_type}&{client_id}&{redirect_uri}&{scope}&{access_type}',
    }


@router.get('/login', dependencies=[anonymous_user])
async def auth_google(
    code: str,
    db: session,
    settings: Annotated[Settings, Depends(get_settings)],
):
    # get token data
    token_url = 'https://accounts.google.com/o/oauth2/token'
    data = {
        'code': code,
        'client_id': settings.google_client_id,
        'client_secret': settings.google_client_secret,
        'redirect_uri': settings.google_redirect_uri,
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=data).json()
    
    # get access token and decode it

    # get user info
    access_token = response.get('access_token')
    user_info = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo', 
        headers={'Authorization': f'Bearer {access_token}'},
    ).json()
    google_id = user_info.get('id')
    email = user_info.get('email')

    # check if user exists
    query = select(User).where(User.email == email)
    user = (await db.execute(query)).scalar()
    
    if not user:
        return {
            'url': 'http://localhost:8000/google-auth/register',
            'email': email,
            'google_id': google_id,
        }
    else:
        if user.provider != 'google':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User already exists.'
            )
        data = {'obj': 'google_user', 'name': user.username}
        access_token = JWT.create_token(data)
        refresh_token = JWT.create_token(data, exp_time=1440)
        return Token(access_token=access_token, refresh_token=refresh_token)


@router.post(
    path='/register',
    status_code=status.HTTP_201_CREATED,
    dependencies=[anonymous_user],
    response_model=UserSocialRegister,
)
async def register_google(
    db: session,
    form: UserSocialRegister,
    avatar: UploadFile | None = None,
):  
    # generate data
    data = form.model_dump()
    data['provider'] = 'google'
    data['is_active'] = True
    if avatar:
        path = 'media/users/'
        data['avatar'] = await generate_image_path(path, avatar)

    # create user
    try:
        db.add(User(**data))
        await db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists.'
        )
    return UserSocialRegister(**data)
