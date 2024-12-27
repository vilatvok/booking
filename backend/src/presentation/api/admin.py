from sqladmin import ModelView

from src.infrastructure.models.offers import Offer, Feedback, Image, Price
from src.infrastructure.models.users import User, Company
from src.infrastructure.models.chats import Chat, Message


class BaseAdmin(ModelView):
    column_list = '__all__'


class UserAdmin(BaseAdmin, model=User):
    pass
    

class CompanyAdmin(BaseAdmin, model=Company):
    pass


class OfferAdmin(BaseAdmin, model=Offer):
    pass


class FeedbackAdmin(BaseAdmin, model=Feedback):
    pass


class ImageAdmin(BaseAdmin, model=Image):
    pass


class PriceAdmin(BaseAdmin, model=Price):
    pass


class ChatAdmin(BaseAdmin, model=Chat):
    pass


class MessageAdmin(BaseAdmin, model=Message):
    pass
