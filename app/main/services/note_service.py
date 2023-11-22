import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main.models.db_models import Note


async def save_note(db: AsyncSession, note):
    logging.info(f"Creating new note...\n{note}")
    new_note = Note(
        title=note.title, description=note.description, target_date=note.target_date
    )
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    logging.info("Note has been successfully saved to the DB!")
    return new_note


async def fetch_all_notes(db: AsyncSession):
    logging.info("Fetching all saved notes...")
    notes = await db.execute(select(Note).where(Note.is_deleted == False))
    return notes.scalars().all()


async def update_note_by_id(db: AsyncSession, note_id: int, note):
    pass
