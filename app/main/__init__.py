import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status

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
    docs_url=constants.API_DOCS_URL,
    redoc_url=constants.API_REDOCS_URL,
    contact={"name": "Shaik Malik Basha", "email": "shaikmalikbasha@example.com"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
)


# @app.get("/", status_code=status.HTTP_200_OK)
# async def index(req: Request):
#     host: str = f"{req.url.scheme}://{req.url.hostname}:{req.url.port}"

#     return {
#         "success": True,
#         "docs": host + constants.API_DOCS_URL,
#         "redoc": host + constants.API_REDOCS_URL,
#     }


@app.get("/", status_code=status.HTTP_200_OK)
async def index(req: Request):
    host: str = f"{req.url.scheme}://{req.url.hostname}:{req.url.port}"
    logging.info(f"Root Endpoint: {host}")

    return {
        "success": True,
        "docs": constants.API_DOCS_URL,
        "redoc": constants.API_REDOCS_URL,
    }


## Root Mapping for all the endpoints
app.include_router(route_mapper, prefix=constants.API_VERSION)
