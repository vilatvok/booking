from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.services.routers import router as service_router
from src.auth.routers.users import router as user_router
from src.auth.routers.enterprises import router as enterprise_router
from src.auth.routers.settings import router as settings_router


app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(service_router, tags=['services'], prefix='/services')
app.include_router(user_router, tags=['users'], prefix='/users')
app.include_router(settings_router, tags=['settings'], prefix='/settings')
app.include_router(
    enterprise_router,
    tags=['enterprises'],
    prefix='/enterprises',
)
