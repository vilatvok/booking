from typing import Annotated
from fastapi import Form, status, APIRouter

from src.application.dtos.offers import OfferSchema
from src.application.dtos.users import UserComplete
from src.application.dtos.companies import (
    CompanyRegister,
    CompanySchema,
    CompanyUpdate,
)
from src.presentation.api.dependencies.usecases import company_usecase
from src.presentation.api.dependencies.users import current_user


router = APIRouter()


@router.post(
    path='/register',
    dependencies=[],
    status_code=status.HTTP_200_OK,
)
async def registration(
    current_user: Annotated[UserComplete, current_user],
    company_usecase: company_usecase,
    form_data: Annotated[CompanyRegister, Form(media_type="multipart/form-data")],
):
    return await company_usecase.register_company(current_user.id, form_data)


@router.get('/', response_model=list[CompanySchema])
async def get_companies(company_usecase: company_usecase):
    return await company_usecase.get_companies()


@router.get('/{name}', response_model=CompanySchema)
async def get_company(name: str, company_usecase: company_usecase):
    return await company_usecase.get_company(name)


@router.get('/{name}/offers', response_model=list[OfferSchema])
async def get_company_offers(name: str, company_usecase: company_usecase):
    return await company_usecase.get_company_offers(name)


@router.patch(
    path='/me',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CompanySchema,
)
async def update_company(
    company_usecase: company_usecase,
    current_user: Annotated[UserComplete, current_user],
    form_data: Annotated[CompanyUpdate, Form(media_type="multipart/form-data")],
):
    return await company_usecase.update_company(current_user.id, form_data)


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_usecase: company_usecase,
    current_user: Annotated[UserComplete, current_user],
):
    return await company_usecase.delete_company(current_user.id)
