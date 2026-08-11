from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.schemas import NoteResponse, NoteCreate, NoteUpdate
from app.services.note_service import get_all_notes,get_note_by_id,create_new_note,update_note,delete_note

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model = list[NoteResponse])
def get_all_notes_endpoint(db : Session = Depends(get_db)):
    note = get_all_notes(db)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes available")
    return note

@router.get("/{note_id}", response_model = NoteResponse)
def get_note_by_id_endpoint(note_id: int, db: Session = Depends(get_db)):
    note = get_note_by_id(note_id, db)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.post("/", response_model = NoteResponse)
def create_new_note_endpoint(note_data: NoteCreate, db: Session = Depends(get_db)):
    return create_new_note(note_data, db)

@router.put("/{note_id}", response_model = NoteResponse)
def update_note_endpoint(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    note_db_response = update_note(note_id, note, db)
    if note.title is None and note.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field (title or content) must be provided for update")
    elif not note_db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note_db_response

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    note_db_response = delete_note(note_id, db)
    if not note_db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None