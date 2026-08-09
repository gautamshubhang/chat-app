from fastapi import APIRouter
from app.services.note_service import get_all_notes,get_note_by_id,create_new_note,update_note,delete_note

router = APIRouter(prefix="/notes", tags=["Notes"])


router.get("/")(get_all_notes)

router.get("/{note_id}")(get_note_by_id)

router.post("/")(create_new_note)

router.put("/{note_id}")(update_note)

router.delete("/{note_id}")(delete_note)