import logging
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.main.models.db_models import Note
from app.main.schemas.note_schema import CreateNote


async def get_notes_count(db: AsyncSession) -> int:
    logging.info("Fetching notes count...")
    ## Method - 1
    stmt1 = (
        select(text("COUNT(*) as total"))
        .select_from(Note)
        .where(Note.is_deleted.is_(False))
    )
    print("SQLAlchemy Statement: ", stmt1)

    # ## Method - 2
    # stmt2 = text("SELECT COUNT(*), MAX(id) FROM notes WHERE is_deleted = :is_deleted")
    # print("SQLAlchemy Statement: ", stmt2)

    # ## Method - 3
    # stmt3 = (
    #     select(
    #         func.count().label("total"),  # COUNT(*) as total
    #         func.max(Note.id).label("max_id"),  # MAX(id) as max_id
    #     )
    #     .select_from(Note)
    #     .where(Note.is_deleted.is_(False))
    # )
    # print("SQLAlchemy Statement: ", stmt3)

    result = await db.execute(stmt1, {"is_deleted": False})
    count = result.scalar_one()  ## We have to use fetchone() which returns a tuple
    logging.info(f"Notes count: {count}")
    return count


async def save_note(db: AsyncSession, note: CreateNote):
    logging.info(f"Creating new note...\n{note}")
    new_note = Note(
        title=note.title,
        description=note.description,
        target_date=note.target_date,
        user_id=note.user_id,
    )
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    logging.info("Note has been successfully saved to the DB!")
    return new_note


async def fetch_all_notes(db: AsyncSession, offset: int, limit: int) -> Sequence[Note]:
    logging.info("Fetching all saved notes...")
    notes = await db.execute(
        select(Note)
        .where(Note.is_deleted.is_(False))
        .offset(offset=offset)
        .limit(limit=limit)
    )
    return notes.scalars().all()


async def fetch_note_by_id(db: AsyncSession, note_id: int):
    logging.info(f"Fetching Note with id: '{note_id}' from the database...")
    stmt = select(Note).where(Note.id == note_id).where(Note.is_deleted.is_(False))
    result = await db.execute(stmt)
    db_note = result.scalar_one_or_none()

    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "Bad Request",
                "description": "Note Not Found",
                "ui_message": f"Note with id:'{note_id}' doesn't exist",
            },
        )
    return db_note


async def update_note_by_id(db: AsyncSession, note_id: int, note):
    logging.info(f"Updating Note by id: '{note_id}'...")

    db_note = await fetch_note_by_id(db, note_id)

    updates = {}
    for key, value in note:
        if value is not None:
            updates[key] = value

    update_stmt = update(Note).where(Note.id == note_id).values(**updates)
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
    await db.refresh(db_note)
    return db_note


async def remove_note_by_id(db: AsyncSession, note_id: int):
    logging.info(f"Deleting Note by id: '{note_id}'...")
    db_note = await fetch_note_by_id(db, note_id)

    delete_stmt = update(Note).where(Note.id == note_id).values(is_deleted=True)
    print(delete_stmt)
    await db.execute(delete_stmt)
    await db.commit()
    await db.refresh(db_note)

    return db_note
