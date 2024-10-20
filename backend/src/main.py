import contextlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from src.admin import (
    ChatAdmin,
    UserAdmin,
    EnterpriseAdmin,
    ServiceAdmin,
    FeedbackAdmin,
    ImageAdmin,
    PriceAdmin,
    MessageAdmin,
)
from src.database import session_manager
from src.routers.services import router as service_router
from src.routers.auth import router as auth_router
from src.routers.users import router as user_router
from src.routers.settings import router as settings_router
from src.routers.enterprises import router as enterprise_router
from src.routers.google_auth import router as google_auth_router
from src.routers.chats import router as chat_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Close the database connection when the app is shut down."""
    yield
    if session_manager._engine is not None:
        await session_manager.close()


app = FastAPI(lifespan=lifespan)


# add cors for react app
origins = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# mount static and media files
app.mount('/static', StaticFiles(directory='src/static'), name='static')
app.mount('/media', StaticFiles(directory='src/media'), name='media')


# add routes
app.include_router(service_router, tags=['services'], prefix='/services')
app.include_router(auth_router, tags=['auth'], prefix='/auth')
app.include_router(user_router, tags=['users'], prefix='/users')
app.include_router(google_auth_router, tags=['google'], prefix='/google-auth')
app.include_router(settings_router, tags=['settings'], prefix='/settings')
app.include_router(chat_router, tags=['chats'], prefix='/chats')
app.include_router(
    enterprise_router,
    tags=['enterprises'],
    prefix='/enterprises',
)


# admin site
admin = Admin(app, session_manager._engine)
admin.add_view(UserAdmin)
admin.add_view(EnterpriseAdmin)
admin.add_view(ServiceAdmin)
admin.add_view(FeedbackAdmin)
admin.add_view(ImageAdmin)
admin.add_view(PriceAdmin)
admin.add_view(ChatAdmin)
admin.add_view(MessageAdmin)
