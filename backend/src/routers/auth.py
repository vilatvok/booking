from fastapi import APIRouter, HTTPException
from sqlalchemy import select, update

from src.models.enterprises import Enterprise
from src.models.users import User
from src.schemas.tokens import Token, RefreshToken
from src.schemas.auth import PasswordReset, PasswordResetConfirm
from src.dependencies import redis_session, db_session, anonymous_user
from src.utils.auth import Password
from src.utils.tokens import JWT
from src.celery import send_password_reset


router = APIRouter()


@router.post('/token/refresh', response_model=Token)
async def update_token(rdb: redis_session, form: RefreshToken):
    data = {}
    if form.username:
        data['obj'] = 'user'
        data['name'] = form.username
    elif form.enterprise:
        data['obj'] = 'enterprise'
        data['name'] = form.enterprise

    if not data:
        data = JWT.decode_token(form.refresh_token, rdb=rdb)
        access = JWT.create_token(data)
        return Token(access_token=access)
    else:
        access = JWT.create_token(data)
        refresh = JWT.create_token(data, exp_time=1440)
        return Token(access_token=access, refresh_token=refresh)


@router.post(
    path='/password-reset',
    status_code=202,
    dependencies=[anonymous_user],
)
async def password_reset(db: db_session, form: PasswordReset):
    model = form.model.value
    email = form.email
    model = User if model == 'user' else Enterprise
    
    # check if object exists
    query = select(model).where(model.email == email)
    obj = (await db.execute(query)).scalar()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f'{model.__name__} not found',
        )

    # generate data for token
    data = {'model': model, 'email': email}

    # send email with password reset link
    send_password_reset.apply_async(args=[email, data])
    return {'status': 'Check your email for password reset link.'}

    
@router.patch(
    path='/password-reset/{token}',
    status_code=200,
    dependencies=[anonymous_user],
)
async def password_reset_confirm(
    db: db_session,
    token: str,
    form: PasswordResetConfirm
):
    # validate password
    pswd1 = form.password1
    pswd2 = form.password2
    if pswd1 != pswd2:
        raise HTTPException(status_code=400, detail='Passwords do not match')
    pswd = Password.generate(pswd1)

    # decode token
    data = JWT.decode_token(token)
    model = data['model']
    email = data['email']

    # try to update password
    model = User if model == 'user' else Enterprise
    stmt = (
        update(model).
        where(model.email == email).
        values(password=pswd).
        returning(model.id)
    )
    obj = (await db.execute(stmt)).fetchone()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=f'{model.__name__} not found',
        )

    await db.commit()
    return {'status': 'Password has been changed'}
