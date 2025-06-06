import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, responses, status
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

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


# Mount /static path to the ./static folder
app.mount("/static", StaticFiles(directory="app/main/static"), name="static")
templates = Jinja2Templates(directory="app/main/templates")

app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.exception_handler(Exception)
def internal_server_error(req: Request, e: Exception):
    desc = "Please contact the support team for further assistance."

    try:
        desc = getattr(e, "message", repr(e))
    except Exception as e:
        msg = traceback.format_exc(limit=4)
        logging.warning(msg)

    return responses.JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal Server Error",
            "description": desc,
        },
    )


@app.get("/", status_code=status.HTTP_200_OK, tags=["Index API"])
async def index(req: Request):
    # host: str = f"{req.url.scheme}://{req.url.hostname}:{req.url.port}"
    return templates.TemplateResponse(
        "index.html",
        {
            "request": req,
            "name": constants.APP_NAME,
        },
    )
    # return {
    #     "success": True,
    #     "docs": host + constants.API_DOCS_URL,
    #     "redoc": host + constants.API_REDOCS_URL,
    # }


app.include_router(route_mapper, prefix=constants.API_VERSION)
