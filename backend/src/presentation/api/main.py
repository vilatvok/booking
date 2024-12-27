import logging
import contextlib

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from src.application.exceptions import (
    InvalidDataError,
    NotFoundError,
    RepositoryError,
    AlreadyExistsError,
    ValidationError,
)
from src.infrastructure.database import session_manager
from src.presentation.api.dependencies.scheduler import scheduler
from src.presentation.api.admin import (
    ChatAdmin,
    UserAdmin,
    CompanyAdmin,
    OfferAdmin,
    FeedbackAdmin,
    ImageAdmin,
    PriceAdmin,
    MessageAdmin,
)
from src.presentation.api.routers.offers import router as offer_router
from src.presentation.api.routers.users import router as user_router
from src.presentation.api.routers.companies import router as company_router
from src.presentation.api.routers.auth import router as auth_router
from src.presentation.api.routers.chats import router as chat_router


logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
    if session_manager._engine is not None:
        await session_manager.close()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RepositoryError)
async def repository_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={'message': str(exc)},
    )


@app.exception_handler(InvalidDataError)
async def invalid_data_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={'message': str(exc)},
    )


@app.exception_handler(AlreadyExistsError)
async def already_exists_error_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={'message': str(exc)},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={'message': str(exc)},
    )


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={'message': str(exc)},
    )


@app.exception_handler(PermissionError)
async def permission_error_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content={'message': str(exc)},
    )


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
app.include_router(offer_router, tags=['offers'], prefix='/offers')
app.include_router(user_router, tags=['users'], prefix='/users')
app.include_router(auth_router, tags=['auth'], prefix='/auth')
app.include_router(chat_router, tags=['chats'], prefix='/chats')
app.include_router(
    company_router,
    tags=['companies'],
    prefix='/companies',
)


# admin site
admin = Admin(app, session_manager._engine)
admin.add_view(UserAdmin)
admin.add_view(CompanyAdmin)
admin.add_view(OfferAdmin)
admin.add_view(FeedbackAdmin)
admin.add_view(ImageAdmin)
admin.add_view(PriceAdmin)
admin.add_view(ChatAdmin)
admin.add_view(MessageAdmin)
