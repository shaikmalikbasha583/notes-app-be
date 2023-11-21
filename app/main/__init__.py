from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.main.config.db_config import initialize_db
from app.main.routers.mapper import route_mapper
from app.main.utils import constants


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_db()
    yield


app = FastAPI(
    title=constants.APP_NAME,
    summary=constants.APP_SUMMARY,
    description=constants.APP_DESC,
    version=constants.APP_VERSION,
    contact={"name": "Shaik Malik Basha", "email": "shaikmalikbasha@example.com"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

app.include_router(route_mapper, prefix=constants.API_VERSION)
