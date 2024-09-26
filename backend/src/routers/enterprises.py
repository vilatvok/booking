from typing import Annotated

from pydantic import EmailStr
from fastapi import Depends, Form, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.datastructures import UploadFile
from sqlalchemy import select, update

from src.exceptions import not_found
from src.utils.common import generate_image_path
from src.utils.auth import AuthEnterprise
from src.utils.tokens import JWT
from src.dependencies import anonymous_user, current_user, session
from src.schemas.tokens import Token
from src.schemas.enterprises import EnterpriseRegister, EnterpriseSchema
from src.models.enterprises import Enterprise
from src.exceptions import not_found


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[anonymous_user],
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    db: session,
    form: EnterpriseRegister,
    logo: UploadFile | None = None,
):
    return await AuthEnterprise.registration(db, form, logo)


@router.get('/register-confirm/{token}', status_code=status.HTTP_201_CREATED)
async def confirm_registration(token: str, db: session):
    return await AuthEnterprise.confirm_registration(token, db)


@router.post(
    path='/login',
    dependencies=[anonymous_user],
    response_model=Token,
)
async def login(db: session, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    enterprise = await AuthEnterprise.authenticate(
        db=db,
        email=form.username,
        password=form.password,
    )
    data = {'enterprise': enterprise.name}
    access = JWT.create_token(data)
    refresh = JWT.create_token(data, exp_time=1440)
    return Token(access_token=access, refresh_token=refresh)


@router.get('/{name}', response_model=EnterpriseSchema)
async def get_enterprise(db: session, name: str):
    query = (await db.execute(
        select(Enterprise).
        where(Enterprise.name == name)
    )).scalar()
    if not query:
        raise not_found
    return query


@router.get('/', response_model=list[EnterpriseSchema])
async def get_enterprises(db: session):
    query = (await db.execute(select(Enterprise))).scalars().all()
    return query


@router.patch('/me', status_code=status.HTTP_202_ACCEPTED)
async def edit_enterprise(
    db: session,
    current_user: Annotated[EnterpriseSchema, current_user],
    name: Annotated[str | None, Form()] = None,
    owner: Annotated[str | None, Form()] = None,
    email: Annotated[EmailStr | None, Form()] = None,
    logo: UploadFile | None = None,
):
    if not hasattr(current_user, 'name'):
        raise not_found

    data = {}
    if name:
        data['name'] = name
    if owner:
        data['owner'] = owner
    if email:
        data['email'] = email
    if logo:
        path = 'media/users/'
        logo = await generate_image_path(path, logo)
        data['logo'] = logo

    stmt = (
        update(Enterprise).
        values(data).
        where(Enterprise.id == current_user.id)
    )
    
    await db.execute(stmt)
    await db.commit()

    return {'status': 'Updated'}
