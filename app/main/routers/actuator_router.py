import logging

from fastapi import APIRouter

from app.main.services.actuator_service import get_app_info

actuator_router = APIRouter(prefix="/actuator", tags=["Actuator"])


@actuator_router.get("/info")
async def info():
    return get_app_info()
