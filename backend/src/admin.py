from sqladmin import ModelView

from src.models.services import Feedback, Image, Price, Service
from src.models.users import User
from src.models.enterprises import Enterprise
from src.models.chats import Chat, Message


class BaseAdmin(ModelView):
    column_list = '__all__'


class UserAdmin(BaseAdmin, model=User):
    pass
    

class EnterpriseAdmin(BaseAdmin, model=Enterprise):
    pass


class ServiceAdmin(BaseAdmin, model=Service):
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
