"""
This Class is not in USE

"""

import logging
from typing import List, Optional, Type, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

# Define a generic type for models
T = TypeVar("T")


class CRUDService:
    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: T) -> T:
        """
        Create a new record in the database.
        """
        logging.info(f"Creating new {self.model.__name__}...{obj_in}")
        db_obj = self.model(**obj_in.dict())  # Assuming the input is a Pydantic model
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        logging.info(f"{self.model.__name__} has been successfully saved to the DB!")
        return db_obj

    async def get_all(self, db: AsyncSession, offset: int, limit: int) -> List[T]:
        """
        Fetch all records, applying pagination.
        """
        logging.info(f"Fetching all {self.model.__name__}s from the database...")
        stmt = (
            select(self.model)
            .where(self.model.is_deleted.is_(False))
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, entity_id: int) -> Optional[T]:
        """
        Fetch a record by its ID.
        """
        logging.info(f"Fetching {self.model.__name__} with ID: {entity_id}...")
        stmt = (
            select(self.model)
            .where(self.model.id == entity_id)
            .where(self.model.is_deleted.is_(False))
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, entity_id: int, obj_in: T) -> T:
        """
        Update an existing record.
        """
        db_obj = await self.get_by_id(db, entity_id)

        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Bad Request",
                    "description": f"{self.model.__name__} Not Found",
                    "ui_message": f"{self.model.__name__} with id:{entity_id} doesn't exist",
                },
            )

        updates = {}
        for key, value in obj_in.dict(
            exclude_unset=True
        ).items():  # exclude_unset ensures only fields sent are updated
            if value is not None:
                updates[key] = value

        if len(updates) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Bad Request",
                    "description": "Insufficient Details",
                    "ui_message": "Please provide valid details",
                },
            )

        stmt = update(self.model).where(self.model.id == entity_id).values(**updates)
        await db.execute(stmt)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, entity_id: int) -> T:
        """
        Soft delete a record (set is_deleted=True).
        """
        db_obj = await self.get_by_id(db, entity_id)

        if db_obj is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "message": "Bad Request",
                    "description": f"{self.model.__name__} Not Found",
                    "ui_message": f"{self.model.__name__} with id:{entity_id} doesn't exist",
                },
            )

        stmt = (
            update(self.model).where(self.model.id == entity_id).values(is_deleted=True)
        )
        await db.execute(stmt)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
