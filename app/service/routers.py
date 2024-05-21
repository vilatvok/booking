from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status, UploadFile

from sqlalchemy import select, update, and_, delete, insert, func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from app.database import session
from app.service import schemas
from app.service.models import Service, Prices, Feedback, Image
from app.auth.models import User, Enterprise
from app.auth.dependencies import current_user
from app.exceptions import not_found, permission_required

router = APIRouter()


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_service(
    db: session,
    user: Annotated[User | Enterprise, current_user],
    images: list[UploadFile],
    service: Annotated[schemas.ServiceCreate, Body()],
):
    user_id = user.get('user_id')
    enter_id = user.get('enter_id')
    if user_id:
        obj = user_id
    else:
        obj = enter_id

    stmt = await db.execute(
        insert(Service).
        values({**service.model_dump(exclude=['prices']), 'owner_id': obj}).
        returning(Service)
    )
    stmt_id = stmt.scalar().id
    await db.execute(
        insert(Prices).
        values({**service.prices.model_dump(), 'service_id': stmt_id})
    )

    folder = 'app/service/media/'

    for image in images:
        if image.content_type not in ['image/jpeg', 'image/png']:
            raise HTTPException(400, 'Invalid content type')

        path = folder + image.filename
        with open(path, 'wb') as f:
            f.write(await image.read())

        await db.execute(
            insert(Image).values(data=str(path), service_id=stmt_id)
        )
    await db.commit()
    return {'status': 'Ok'}


@router.get('/', response_model=list[schemas.Service])
async def get_services(db: session):
    query = (await db.execute(
        select(Service, Prices).
        options(joinedload(Service.owner)).
        join(Service.owner).
        join(Service.prices)
    )).all()

    services_with_prices = []

    for service, prices in query:
        images = (await db.execute(
            select(Image.data).
            where(Image.service_id == service.id)
        )).all()
        services = {
            'id': service.id,
            'owner': service.owner.username,
            'name': service.name,
            'description': service.description,
            'type': service.type.value,
            'city': service.city,
            'phone': service.phone,
            'images': [image for image in images],
            'prices': {
                'per_hour': prices.per_hour,
                'per_day': prices.per_day,
                'per_month': prices.per_month,
                'per_year': prices.per_year,
            },
        }
        services_with_prices.append(services)

    return services_with_prices


@router.get('/{service_id}', response_model=schemas.ServiceOne)
async def get_service(service_id: int, db: session):
    service = (await db.execute(
        select(
            Service,
            User.username,
            Prices,
            func.round(func.avg(Feedback.rating), 1).label('avg_rating'),
        ).join(Service.owner).
        join(Service.prices).
        join(Service.feedbacks, isouter=True).
        group_by(Service, User.username, Prices).
        where(Service.id == service_id)
    )).first()

    if not service:
        raise not_found

    feedbacks = (await db.execute(
        select(Feedback).
        options(joinedload(Feedback.user)).
        join(Feedback.user).
        join(Feedback.service).
        where(Service.id == service_id)
    )).scalars().all()

    images = (await db.execute(
        select(Image).
        join(Image.service).
        where(Service.id == service_id)
    )).scalars().all()

    service = service[0]
    user = service[1]
    prices = service[2]
    avg_rating = service[3]

    images = [
        {
            'data': image.data,
        } for image in images
    ]

    prices = {
        'per_hour': prices.per_hour,
        'per_day': prices.per_day,
        'per_month': prices.per_month,
        'per_year': prices.per_year,
    }
    feedbacks = [
        {
            'user': feedback.user.username,
            'rating': feedback.rating,
            'text': feedback.text,
            'created': feedback.created,
        } for feedback in feedbacks
    ]
    result = {
        'id': service.id,
        'owner': user,
        'name': service.name,
        'description': service.description,
        'type': service.type.value,
        'city': service.city,
        'phone': service.phone,
        'images': images,
        'prices': prices,
        'avg_rating': avg_rating if avg_rating else 0,
        'feedbacks': feedbacks,
    }
    return result


@router.patch('/{service_id}/update', status_code=status.HTTP_202_ACCEPTED)
async def update_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: session,
    user: Annotated[User | Enterprise, current_user],
):
    service_ = (await db.execute(
        select(Service).
        where(and_(Service.id == service_id))
    )).scalar()

    if not service_:
        raise not_found

    user_id = user.get('user_id')
    enterprise_id = user.get('enter_id')

    if user_id:
        if user_id != service_.owner_id:
            raise permission_required
    else:
        if enterprise_id != service_.owner_id:
            raise permission_required

    await db.execute(
        update(Service).
        where(Service.id == service_id).
        values(service.model_dump(exclude=['prices'], exclude_unset=True))
    )

    if service.prices:
        await db.execute(
            update(Prices).
            where(Prices.service_id == service_id).
            values(service.prices.model_dump(exclude_unset=True))
        )
    await db.commit()
    return service


@router.delete('/{service_id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    db: session,
    user: Annotated[User | Enterprise, current_user],
):
    service = (await db.execute(
        select(Service).
        where(and_(Service.id == service_id))
    )).scalar()

    if not service:
        raise not_found

    user_id = user.get('user_id')
    enterprise_id = user.get('enter_id')

    if user_id:
        if user_id != service.owner_id:
            raise permission_required
    else:
        if enterprise_id != service.owner_id:
            raise permission_required

    await db.execute(delete(Service).where(Service.id == service_id))
    await db.commit()
    return {'status': 'Ok'}


@router.post(
    '/{service_id}/feedback/create',
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    service_id: int,
    feedback: schemas.FeedbackCreate,
    user: Annotated[User | Enterprise, current_user],
    db: session,
):
    user_id = user.get('user_id')
    try:
        await db.execute(
            insert(Feedback).
            values(
                {
                    **feedback.model_dump(),
                    'user_id': user_id,
                    'service_id': service_id,
                }
            )
        )
    except IntegrityError:
        raise permission_required
    else:
        await db.commit()
    return {'status': 'created'}
