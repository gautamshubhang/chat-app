from app.database import get_db, note_db
from app.model import Note
from fastapi import status, HTTPException, Depends
from app.schemas import NoteCreate, NoteResponse,NoteUpdate
from datetime import datetime
from sqlalchemy import select, func



def get_all_notes(db=Depends(get_db)):
    stmt = select(Note)
    note = db.execute(stmt).all()
    return note

def get_note_by_id(note_id: int,db=Depends(get_db)):
    stmt = select(Note).where(Note.id == note_id)
    note = db.execute(stmt).scalars().first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


def create_new_note(note_data:NoteCreate,db=Depends(get_db)):
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return {"message": "Note created successfully", "note":new_note}

def update_note(note_id: int, note: NoteUpdate, db=Depends(get_db)):
    stmt = select(Note).where(Note.id == note_id)
    note_db_response = db.execute(stmt).scalars().first()
    if not note_db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    elif note.title is None and note.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field (title or content) must be provided for update")
    updated_note = note.model_dump(exclude_unset=True)
    for key, value in updated_note.items():
        setattr(note_db_response, key, value)
    db.commit()
    db.refresh(note_db_response)
    return {"message": "Note updated successfully", "note": note_db_response}

def delete_note(note_id: int, db=Depends(get_db)):
    stmt = select(Note).where(Note.id == note_id)
    note_db_response = db.execute(stmt).scalars().first()
    if not note_db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note_db_response)
    db.commit()
    return None