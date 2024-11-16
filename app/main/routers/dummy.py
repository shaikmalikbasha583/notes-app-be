"""
This Router is not in USE

"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.main.config.db_config import AsyncSession, get_db_async
from app.main.models.db_models import User
from app.main.schemas.user_schema import CreateUser, UpdateUser
from app.main.services.crud_service import CRUDService

router = APIRouter()

user_crud_service = CRUDService(User)


@router.post("/users/", response_model=User)
async def create_user(user_in: CreateUser, db: AsyncSession = Depends(get_db_async)):
    return await user_crud_service.create(db=db, obj_in=user_in)


@router.get("/users/", response_model=List[User])
async def get_users(
    offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_async)
):
    return await user_crud_service.get_all(db=db, offset=offset, limit=limit)


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_async)):
    user = await user_crud_service.get_by_id(db=db, entity_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int, user_in: UpdateUser, db: AsyncSession = Depends(get_db_async)
):
    return await user_crud_service.update(db=db, entity_id=user_id, obj_in=user_in)


@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_async)):
    return await user_crud_service.delete(db=db, entity_id=user_id)
