from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.service.routers import router as service_router
from app.auth.routers import user_router, enterprise_router, settings_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(service_router, tags=['services'], prefix='/services')
app.include_router(user_router, tags=['users'], prefix='/users')
app.include_router(enterprise_router, tags=['enterprises'], prefix='/enterprises')
app.include_router(settings_router, tags=['settings'], prefix='/settings')