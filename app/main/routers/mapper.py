from fastapi import APIRouter

from .actuator_router import actuator_router
from .user_router import user_router

route_mapper = APIRouter()


## Mapping Actuator
route_mapper.include_router(actuator_router)
route_mapper.include_router(user_router)
