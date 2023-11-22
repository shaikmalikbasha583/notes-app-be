from fastapi import APIRouter

from .actuator_router import actuator_router
from .user_router import user_router
from .note_router import note_router

route_mapper = APIRouter()


## Mapping Actuator Routes/Resources
route_mapper.include_router(actuator_router)

## Mapping User Routes/Resources
route_mapper.include_router(user_router)

## Mapping Note Routes/Resources
route_mapper.include_router(note_router)
