from sqlalchemy.orm import Session
from app.model import Note
from app.schemas.note_schemas import NoteCreate,NoteUpdate
from sqlalchemy import select



def get_all_notes(db : Session):
    stmt = select(Note)
    return db.execute(stmt).scalars().all()

def get_note_by_id(note_id: int,db : Session):
    stmt = select(Note).where(Note.id == note_id)
    return db.execute(stmt).scalars().first()


def create_new_note(note_data:NoteCreate,db : Session):
    new_note = Note(
        title=note_data.title,
        content=note_data.content,
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def update_note(note_id: int, note: NoteUpdate, db : Session):
    stmt = select(Note).where(Note.id == note_id)
    note_db_response = db.execute(stmt).scalars().first()
    if not note_db_response:
        return None
    updated_note = note.model_dump(exclude_unset=True)
    for key, value in updated_note.items():
        setattr(note_db_response, key, value)
    db.commit()
    db.refresh(note_db_response)
    return note_db_response

def delete_note(note_id: int, db : Session):
    stmt = select(Note).where(Note.id == note_id)
    note_db_response = db.execute(stmt).scalars().first()
    if not note_db_response:
        return None
    db.delete(note_db_response)
    db.commit()
    return True