from fastapi import APIRouter
from starlette import status
from app.schemas import NoteResponse
from app.services.note_service import get_all_notes,get_note_by_id,create_new_note,update_note,delete_note

router = APIRouter(prefix="/notes", tags=["Notes"])


router.get("/", response_model = list[NoteResponse])(get_all_notes)

router.get("/{note_id}", response_model = NoteResponse)(get_note_by_id)

router.post("/", response_model = NoteResponse)(create_new_note)

router.put("/{note_id}", response_model = NoteResponse)(update_note)

router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)(delete_note)