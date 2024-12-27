from typing import Annotated
from datetime import datetime, timedelta
from fastapi import BackgroundTasks, Depends, Form, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from apscheduler.triggers.date import DateTrigger

from src.application.dtos.users import (
    UserRegister,
    UserSchema,
    RefreshToken,
    Token,
    UserSocialRegister
)
from src.infrastructure.config import Settings, get_settings
from src.presentation.api.dependencies.scheduler import scheduler
from src.presentation.api.dependencies.users import (
    anonymous_user,
    current_user,
    user_oauth2_scheme,
)
from src.presentation.api.dependencies.usecases import (
    user_social_usecase,
    user_usecase,
)


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[anonymous_user],
    status_code=status.HTTP_200_OK,
)
async def registration(
    user_usecase: user_usecase,
    background: BackgroundTasks,
    form_data: Annotated[UserRegister, Form(media_type="multipart/form-data")],
):
    response = await user_usecase.registration(form_data)
    token_data = response.get('token_data')

    # Send confirmation letter
    background.add_task(user_usecase.send_confirmation_letter, token_data)

    # Delete user if not confirmed in 2 hours
    user_id = token_data.get('user_id')
    scheduler.add_job(
        func=user_usecase.delete_inactive_user,
        trigger=DateTrigger(run_date=datetime.now() + timedelta(hours=2)),
        args=[user_id],
        id=f'delete_inactive_{user_id}',
    )
    return response['message']


@router.get(
    path='/register-confirm/{token}',
    dependencies=[anonymous_user],
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
)
async def confirm_registration(token: str, user_usecase: user_usecase):
    user = await user_usecase.confirm_registration(token)
    scheduler.remove_job(f'delete_inactive_{user.id}')
    return user


@router.post(
    path='/login',
    dependencies=[anonymous_user],
    response_model=Token,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_usecase: user_usecase,
):
    return await user_usecase.login(form_data.username, form_data.password)


@router.post('/logout', dependencies=[current_user])
async def logout(
    token: Annotated[OAuth2PasswordBearer, Depends(user_oauth2_scheme)],
    user_usecase: user_usecase,
):
    return await user_usecase.logout(token)


@router.post('/token/refresh', response_model=Token)
async def update_token(form_data: RefreshToken, user_usecase: user_usecase):
    return await user_usecase.update_token(form_data)


@router.get('/google-auth/link', dependencies=[anonymous_user])
async def google_link(
    settings: Annotated[Settings, Depends(get_settings)],
    user_social_usecase: user_social_usecase,
):
    client_id = settings.google_client_id
    redirect_uri = settings.google_redirect_uri
    return user_social_usecase.get_google_link(client_id, redirect_uri)


@router.get(
    path='/google-auth/login',
    dependencies=[anonymous_user],
    status_code=status.HTTP_200_OK,
)
async def google_authentication(
    code: str,
    settings: Annotated[Settings, Depends(get_settings)],
    user_social_usecase: user_social_usecase,
):
    return await user_social_usecase.google_authentication(
        code=code,
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        redirect_uri=settings.google_redirect_uri,
    )


@router.post(
    path='/google-auth/register',
    status_code=status.HTTP_201_CREATED,
    dependencies=[anonymous_user],
    response_model=UserSchema,
)
async def google_registration(
    form_data: Annotated[UserSocialRegister, Form(media_type="multipart/form-data")],
    user_social_usecase: user_social_usecase,
):  
    return await user_social_usecase.google_registration(form_data)
