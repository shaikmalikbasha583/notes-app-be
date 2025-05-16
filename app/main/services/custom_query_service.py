import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_notes_count(db: AsyncSession) -> int:
    logging.info("Fetching notes count...")
    query = text(
        """SELECT COUNT(1) as total_notes_count FROM notes WHERE 1=1 AND is_deleted = :is_deleted"""
    )
    result = await db.execute(query, {"is_deleted": False})
    return result.scalar_one()
