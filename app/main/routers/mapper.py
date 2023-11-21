from .actuator_router import actuator_router

from fastapi import APIRouter

route_mapper = APIRouter()


## Mapping Actuator
route_mapper.include_router(actuator_router)
