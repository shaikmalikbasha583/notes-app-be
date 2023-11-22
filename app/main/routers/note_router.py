from fastapi import APIRouter, Depends

from app.main.config.db_config import AsyncSession, get_db_async
from app.main.schemas.note_schema import CreateNote
from app.main.services.note_service import fetch_all_notes, save_note

note_router = APIRouter(prefix="/notes", tags=["Note Routers"])


@note_router.get("/")
async def get_all_notes(db: AsyncSession = Depends(get_db_async)):
    notes = await fetch_all_notes(db)
    return notes


@note_router.post("/")
async def add_note(note: CreateNote, db: AsyncSession = Depends(get_db_async)):
    new_note = await save_note(db, note)
    return new_note
