from typing import Annotated

from fastapi import status, APIRouter
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Body

from sqlalchemy import select

from src.database import session
from src.exceptions import not_found
from src.auth import schemas, utils
from src.auth.models import Enterprise
from src.auth.dependencies import anonymous_user
from src.exceptions import not_found


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[anonymous_user],
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    db: session,
    enterprise: Annotated[schemas.EnterpriseRegister, Body()],
    avatar: UploadFile | None = None,
):
    result = await utils.register_response(
        db=db,
        obj=enterprise,
        obj_class=Enterprise,
        avatar=avatar,
    )
    return result


@router.post('/login', dependencies=[anonymous_user])
async def login(db: session, enterprise: schemas.EnterpriseLogin):
    enterprise = await utils.authenticate_enterprise(
        db=db,
        email=enterprise.email,
        password=enterprise.password,
    )
    token = utils.create_token(data={'enter_id': str(enterprise.id)})
    return schemas.Token(access_token=token, token_type='bearer')


@router.get('/{name}', response_model=schemas.Enterprise)
async def get_enterprise(db: session, name: str):
    query = (await db.execute(
        select(Enterprise).
        where(Enterprise.name == name)
    )).scalar()
    if not query:
        raise not_found
    return query
