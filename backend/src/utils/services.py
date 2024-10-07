

class BaseService:
    @staticmethod
    def get_services(services):
        services_with_prices = []
        for service in services:
            owner = service.owner
            username = owner.username if hasattr(owner, 'username') else owner.name
            images = [image for image in service.images]
            prices = service.prices
            services = {
                'id': service.id,
                'owner': username,
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
            services_with_prices.append(services)
        return services_with_prices

    @staticmethod
    def get_user_services(user):
        services_with_prices = []
        services = user.services
        for service in services:
            images = [image for image in service.images]
            prices = service.prices
            services = {
                'id': service.id,
                'owner': user.username,
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
            services_with_prices.append(services)
        return services_with_prices
    
    @staticmethod
    def get_enterprise_services(enterprise):
        services_with_prices = []
        services = enterprise.services
        for service in services:
            images = [image for image in service.images]
            prices = service.prices
            services = {
                'id': service.id,
                'owner': enterprise.owner,
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
            services_with_prices.append(services)
        return services_with_prices