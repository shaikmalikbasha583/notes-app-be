from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.main.config.db_config import AsyncSession, get_db_async
from app.main.schemas.user_schema import CreateUser, UpdateUser
from app.main.services.user_service import (
    fetch_all_users,
    fetch_user_by_id,
    remove_user_by_id,
    save_user,
    update_user_by_id,
)

user_router = APIRouter(prefix="/users", tags=["User Routers"])


@user_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(
    db: AsyncSession = Depends(get_db_async),
    offset: int = 0,
    limit: Annotated[int, Query(le=15)] = 10,
):
    users = await fetch_all_users(db, offset, limit)
    return {
        "success": True,
        "message": "List of users",
        "ui_message": "List of users from the database",
        "users": users,
    }


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_user(user: CreateUser, db: AsyncSession = Depends(get_db_async)):
    new_user = await save_user(db, user)
    return {
        "success": True,
        "message": "New user has been successfully created",
        "ui_message": "New user has been successfully created",
        "created_user": new_user,
    }


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db_async)):
    user = await fetch_user_by_id(db, user_id)
    if user is None:
        return {
            "success": True,
            "message": "User not found",
            "ui_message": f"User with id:'{user_id}' doesn't exist",
            "user": None,
        }

    return {
        "success": True,
        "message": "User details",
        "ui_message": "User details",
        "user": user,
    }


@user_router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
    user_id: int, user: UpdateUser, db: AsyncSession = Depends(get_db_async)
):
    updated_user = await update_user_by_id(db, user_id, user)
    return {
        "success": True,
        "message": "User has been successfully updated",
        "ui_message": "User has been successfully updated",
        "updated_user": updated_user,
    }


@user_router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(get_db_async)):
    deleted_user = await remove_user_by_id(db, user_id)
    return {
        "success": True,
        "message": "User has been successfully deleted!",
        "ui_message": "User has been successfully deleted!",
        "is_deleted": deleted_user.is_deleted,
    }
