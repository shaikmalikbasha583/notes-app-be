import logging

from fastapi import FastAPI

from app.main.utils import constants

app = FastAPI(
    title=constants.APP_NAME,
    summary=constants.APP_SUMMARY,
    description=constants.APP_DESC,
    version=constants.APP_VERSION,
    contact={"name": "Shaik Malik Basha", "email": "shaikmalikbasha@example.com"},
    license_info={"name": "MIT"},
)


@app.get("/")
async def index():
    logging.info("Returning basic information of the app...")
    return {
        "app_name": constants.APP_NAME,
        "app_code": constants.APP_CODE,
        "app_version": constants.APP_VERSION,
    }
