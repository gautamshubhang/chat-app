from app.database import note_db
from fastapi import status, HTTPException
from app.schemas import NotesCreate, NotesResponse,NotesUpdate
from datetime import datetime



def get_all_notes():
    return list(note_db.values())

def get_note_by_id(note_id: int):
    if note_id not in note_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note not found")
    return note_db[note_id]


def create_new_note(note:NotesCreate):
    new_note_id = max(note_db.keys()) + 1 if note_db else 1
    new_note = NotesResponse(
        id=new_note_id,
        title=note.title,
        content=note.content,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    note_db[new_note_id] = new_note
    return {"message": "Note created successfully", "note":new_note}

def update_note(note_id: int, note: NotesUpdate):
    if note_id not in note_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note not found")
    elif note.title is None and note.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field (title or content) must be provided for update")
    updated_note = NotesResponse(
        id=note_id,
        title=note.title if note.title is not None else note_db[note_id].title,
        content=note.content if note.content is not None else note_db[note_id].content,
        created_at=note_db[note_id].created_at,
        updated_at=datetime.now()
    )
    note_db[note_id] = updated_note
    return {"message": "Note updated successfully", "note": updated_note}

def delete_note(note_id: int):
    if note_id not in note_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    del note_db[note_id]
    return {"message": "Note deleted successfully"}