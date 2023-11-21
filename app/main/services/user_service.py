import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main.models.db_models import User


async def save_user(db: AsyncSession, user):
    new_user = User(name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def fetch_all_users(db: AsyncSession):
    results = await db.execute(select(User))
    return results.scalars().all()
