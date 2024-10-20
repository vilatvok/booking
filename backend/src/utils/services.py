from src.models.users import User
from src.models.enterprises import Enterprise


def get_all_services(services) -> list[dict]:
    response = []
    for service in services:
        owner = service.owner
        owner_name = owner.username if hasattr(owner, 'username') else owner.name

        # Generate additional data
        images = [image for image in service.images]
        prices = service.prices

        data = {
            'id': service.id,
            'owner': owner_name,
            'owner_model': owner.__class__.__name__,
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
        }
        response.append(data)
    return response


def get_obj_services(obj: User | Enterprise) -> list[dict]:
    services = obj.services
    response = []
    for service in services:
        images = [image for image in service.images]
        prices = service.prices
        data = {
            'id': service.id,
            'owner': obj.username if hasattr(obj, 'username') else obj.name,
            'owner_model': obj.__class__.__name__,
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
        }
        response.append(data)
    return response