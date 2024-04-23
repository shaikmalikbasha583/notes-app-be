import logging

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.main.models.db_models import User


async def save_user(db: AsyncSession, user):
    new_user = User(name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logging.info("User has been successfully saved to the DB!")
    return new_user


async def fetch_all_users(db: AsyncSession):
    logging.info("Fetching all users from the database...")
    results = await db.execute(select(User).where(User.is_deleted == False))
    return results.scalars().all()


async def update_user_by_id(db: AsyncSession, user_id: int, user):
    db_user = await fetch_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "Bad Request",
                "description": "User Not Found",
                "ui_message": f"User with id:'{user_id}' doesn't exist",
            },
        )

    updates = {}
    for key, value in user:
        if value is not None:
            updates[key] = value

    update_stmt = update(User).where(User.id == user_id).values(**updates)
    print(update_stmt)

    if len(updates) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "Bad Request",
                "description": "Insufficient Details",
                "ui_message": "Please provide the valid details",
            },
        )
    await db.execute(update_stmt)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def fetch_user_by_id(db: AsyncSession, user_id: int):
    logging.info(f"Fetching user with id: '{user_id}' from the database...")
    stmt = select(User).where(User.id == user_id).where(User.is_deleted == False)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def remove_user_by_id(db: AsyncSession, user_id: int):
    db_user = await fetch_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "Bad Request",
                "description": "User Not Found",
                "ui_message": f"User with id:'{user_id}' doesn't exist",
            },
        )

    delete_stmt = update(User).where(User.id == user_id).values(is_deleted=True)

    await db.execute(delete_stmt)
    await db.commit()
    await db.refresh(db_user)
    return db_user
