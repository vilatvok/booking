from typing import Annotated
from fastapi import APIRouter, HTTPException, status, UploadFile
from sqlalchemy import select, update, delete, insert, func
from sqlalchemy.orm import joinedload

from src.exceptions import not_found, permission_required
from src.dependencies import session, current_user, current_service
from src.utils.services import BaseService
from src.utils.common import generate_image_path
from src.models.services import Service, Feedback, Price, Image
from src.models.users import User
from src.models.enterprises import Enterprise
from src.schemas.users import UserSchema
from src.schemas.enterprises import EnterpriseSchema
from src.schemas.services import (
    FeedbackCreate,
    OneService,
    ServiceCreate,
    ServiceSchema,
    ServiceUpdate,
)


router = APIRouter()


@router.get('/', response_model=list[ServiceSchema])
async def get_services(db: session):
    query = (
        select(Service).
        options(
            joinedload(Service.owner).selectin_polymorphic([User, Enterprise]),
            joinedload(Service.images),
            joinedload(Service.prices),
        )
    )
    services = await db.execute(query)
    services = BaseService.get_services(services.unique().scalars().all())
    return services


@router.get('/{service_id}', response_model=OneService)
async def get_service(service_id: int, db: session):
    avg_rating = func.round(func.avg(Feedback.rating), 1).label('avg_rating')
    query = (
        select(Service, avg_rating).
        join(Service.feedbacks).
        options(
            joinedload(Service.owner).selectin_polymorphic([User, Enterprise]),
            joinedload(Service.images),
            joinedload(Service.prices),
            joinedload(Service.feedbacks).joinedload(Feedback.user),
        ).
        where(Service.id == service_id).
        group_by(Service)
    )

    try:
        service, avg_rating = (await db.execute(query)).first()
    except TypeError:
        raise not_found

    owner = service.owner
    prices = service.prices
    images = [image for image in service.images]
    feedbacks = []
    for feedback in service.feedbacks:
        feedbacks.append({
            'user': feedback.user.username,
            'rating': feedback.rating,
            'text': feedback.text,
            'created': feedback.created_at,
        })

    result = {
        'id': service.id,
        'owner': owner.username if hasattr(owner, 'username') else owner.name,
        'name': service.name,
        'description': service.description,
        'type': service.type.value,
        'city': service.city,
        'phone': service.phone,
        'images': images,
        'prices': {
            'per_hour': prices.per_hour,
            'per_day': prices.per_day,
            'per_month': prices.per_month,
            'per_year': prices.per_year,
        },
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
    }
    return result


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_service(
    db: session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    service: ServiceCreate,
    images: list[UploadFile], # This field is optional
):
    # create service
    data = service.model_dump(exclude=['prices'])
    data['owner_id'] = current_user.id
    
    stmt = await db.execute(
        insert(Service).
        values(data).
        returning(Service)
    )
    stmt_id = stmt.scalar().id

    # add prices
    price_data = service.prices.model_dump()
    price_data['service_id'] = stmt_id
    await db.execute(insert(Price).values(price_data))

    # add images
    folder = 'media/services/'
    for image in images:
        if image.content_type not in ['image/jpeg', 'image/png']:
            raise HTTPException(400, 'Invalid content type')

        path = await generate_image_path(folder, image)
        await db.execute(insert(Image).values(data=path, service_id=stmt_id))
    
    # commit all changes
    await db.commit()
    
    return {'status': 'Ok'}


@router.patch('/{service_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_service(
    db: session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    service: Annotated[Service, current_service],
    form: ServiceUpdate,
):  
    if current_user.id != service.owner_id:
        raise permission_required

    data = form.model_dump(exclude=['prices'], exclude_unset=True)
    await db.execute(
        update(Service).
        where(Service.id == service.id).
        values(data)
    )

    if form.prices:
        data = form.prices.model_dump(exclude_unset=True)
        await db.execute(
            update(Price).
            where(Price.service_id == service.id).
            values(data)
        )
    await db.commit()

    return form


@router.delete('/{service_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    db: session,
    current_user: Annotated[UserSchema | EnterpriseSchema, current_user],
    service: Annotated[Service, current_service],
):  
    if current_user.id != service.owner_id:
        raise permission_required

    await db.execute(delete(Service).where(Service.id == service.id))
    await db.commit()
    return {'status': 'Ok'}


@router.post('/{service_id}/feedback', status_code=status.HTTP_201_CREATED)
async def create_feedback(
    db: session,
    current_user: Annotated[UserSchema, current_user],
    service: Annotated[Service, current_service],
    feedback: FeedbackCreate,
):
    data = feedback.model_dump()
    data['user_id'] = current_user.id
    data['service_id'] = service.id
    await db.execute(insert(Feedback).values(data))
    await db.commit()
    return {'status': 'created'}
