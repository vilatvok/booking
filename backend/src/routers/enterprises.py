from typing import Annotated
from pydantic import EmailStr
from fastapi import Depends, Form, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.datastructures import UploadFile
from sqlalchemy import delete, select, update
from sqlalchemy.orm import joinedload

from src.exceptions import not_found
from src.utils.common import generate_image_path
from src.utils.services import get_obj_services
from src.utils.auth import AuthEnterprise
from src.utils.tokens import JWT
from src.dependencies import (
    db_session,
    redis_session,
    anonymous_user,
    current_user,
    enterprise_oauth2_scheme,
)
from src.schemas.tokens import Token
from src.schemas.services import ServiceSchema
from src.schemas.enterprises import EnterpriseRegister, EnterpriseSchema
from src.models.services import Service
from src.models.enterprises import Enterprise
from src.exceptions import not_found


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[anonymous_user],
    status_code=status.HTTP_200_OK,
)
async def registration(
    db: db_session,
    form: EnterpriseRegister,
    logo: UploadFile | None = None,
):
    return await AuthEnterprise.registration(db, form, logo)


@router.get(
    path='/register-confirm/{token}',
    dependencies=[anonymous_user],
    status_code=status.HTTP_201_CREATED,
)
async def confirm_registration(token: str, db: db_session):
    return await AuthEnterprise.confirm_registration(token, db)


@router.post(
    path='/login',
    dependencies=[anonymous_user],
    response_model=Token,
)
async def login(db: db_session, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    enterprise = await AuthEnterprise.authenticate(
        db=db,
        email=form.username,
        password=form.password,
    )
    data = {'obj': 'enterprise', 'id': enterprise.id, 'name': enterprise.name}
    access = JWT.create_token(data)
    refresh = JWT.create_token(data, exp_time=1440)
    return Token(access_token=access, refresh_token=refresh)


@router.get('/', response_model=list[EnterpriseSchema])
async def get_enterprises(db: db_session):
    query = (await db.execute(select(Enterprise))).scalars().all()
    return query


@router.get('/{name}', response_model=EnterpriseSchema)
async def get_enterprise(db: db_session, name: str):
    query = select(Enterprise).where(Enterprise.name == name)
    enterprise = (await db.execute(query)).scalar()
    if not enterprise:
        raise not_found
    return enterprise


@router.get('/{name}/services', response_model=list[ServiceSchema])
async def get_enterprise_services(db: db_session, name: str):
    query = (
        select(Enterprise).
        where(Enterprise.name == name).
        options(
            joinedload(Enterprise.services).joinedload(Service.prices),
            joinedload(Enterprise.services).joinedload(Service.images)
        )
    )

    services = (await db.execute(query)).scalar()
    if not services:
        raise not_found

    return get_obj_services(services)


@router.patch('/me', status_code=status.HTTP_202_ACCEPTED)
async def update_enterprise(
    db: db_session,
    current_user: Annotated[EnterpriseSchema, current_user],
    name: Annotated[str | None, Form()] = None,
    owner: Annotated[str | None, Form()] = None,
    email: Annotated[EmailStr | None, Form()] = None,
    logo: UploadFile | None = None,
):
    data = {}
    if name:
        data['name'] = name
    if owner:
        data['owner'] = owner
    if email:
        data['email'] = email
    if logo:
        path = 'media/users/'
        ava = await generate_image_path(path, logo)
        data['logo'] = ava

    stmt = (
        update(Enterprise).
        values(data).
        where(Enterprise.id == current_user.id).
        returning(Enterprise.id)
    )
   
    obj = await db.execute(stmt)
    if not obj.fetchone():
        raise not_found
    
    await db.commit()
    return {'status': 'Updated'}


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_enterprise(
    db: db_session,
    rdb: redis_session,
    current_user: Annotated[EnterpriseSchema, current_user],
    token: Annotated[str, Depends(enterprise_oauth2_scheme)],
):  
    stmt = delete(Enterprise).where(Enterprise.id == current_user.id)
    await db.execute(stmt)
    await db.commit()

    rdb.sadd('jwt_blacklist', token)

    return {'status': 'Deleted'}
