from fastapi import APIRouter, status

from app.main.services.actuator_service import get_app_info

actuator_router = APIRouter(prefix="/actuator", tags=["Actuator"])


@actuator_router.get("/info", status_code=status.HTTP_200_OK)
async def info():
    return get_app_info()
