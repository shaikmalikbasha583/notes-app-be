import logging

from app.main.utils import constants


def get_app_info():
    logging.info("Fetching basic information of the app...")
    return {
        "app_name": constants.APP_NAME,
        "app_code": constants.APP_CODE,
        "app_version": constants.APP_VERSION,
    }
