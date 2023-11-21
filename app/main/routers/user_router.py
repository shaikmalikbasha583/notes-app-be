import logging

from fastapi import APIRouter, Depends

from app.main.config.db_config import AsyncSession, get_db_async
from app.main.schemas.user_schema import CreateUser
from app.main.services.user_service import fetch_all_users, save_user

user_router = APIRouter(prefix="/users", tags=["User Routers"])


@user_router.get("/")
async def get_all_users(db: AsyncSession = Depends(get_db_async)):
    users = await fetch_all_users(db)
    return users


@user_router.post("/")
async def add_user(user: CreateUser, db: AsyncSession = Depends(get_db_async)):
    new_user = await save_user(db, user)
    return new_user
