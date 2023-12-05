from fastapi import APIRouter, Depends

from app.main.config.db_config import AsyncSession, get_db_async
from app.main.schemas.note_schema import CreateNote, UpdateNote
from app.main.services.note_service import (
    fetch_all_notes,
    fetch_note_by_id,
    remove_note_by_id,
    save_note,
    update_note_by_id,
)

note_router = APIRouter(prefix="/notes", tags=["Note Routers"])


@note_router.get("/")
async def get_all_notes(db: AsyncSession = Depends(get_db_async)):
    notes = await fetch_all_notes(db)
    return {
        "success": True,
        "message": "List of notes",
        "ui_message": "List of notes from the database",
        "notes": notes,
    }


@note_router.post("/")
async def add_note(note: CreateNote, db: AsyncSession = Depends(get_db_async)):
    new_note = await save_note(db, note)
    return {
        "success": True,
        "message": "New Note has been successfully created",
        "ui_message": "New Note has been successfully created",
        "created_note": new_note,
    }


@note_router.get("/{note_id}")
async def get_note_by_id(note_id: int, db: AsyncSession = Depends(get_db_async)):
    db_note = await fetch_note_by_id(db, note_id)
    if db_note is None:
        return {
            "success": True,
            "description": "Note Not Found",
            "ui_message": f"Note with id:'{note_id}' doesn't exist",
            "note": db_note,
        }

    return {
        "success": True,
        "message": "Note Details",
        "ui_message": "Note Details",
        "note": db_note,
    }


@note_router.put("/{note_id}")
async def update_note(
    note_id: int, note: UpdateNote, db: AsyncSession = Depends(get_db_async)
):
    updated_note = await update_note_by_id(db, note_id, note)
    return {
        "success": True,
        "message": "Note has been successfully updated",
        "ui_message": "Note has been successfully updated",
        "updated_note": updated_note,
    }


@note_router.delete("/{note_id}")
async def delete_note_by_id(note_id: int, db: AsyncSession = Depends(get_db_async)):
    deleted_note = await remove_note_by_id(db, note_id)
    return {
        "success": True,
        "message": "Note has been successfully deleted!",
        "ui_message": "Note has been successfully deleted!",
        "is_deleted": deleted_note.is_deleted,
    }
