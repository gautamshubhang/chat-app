from fastapi import APIRouter
from app.services.note_services import get_all_notes,get_note_by_id,create_new_note,update_note,delete_note

router = APIRouter(prefix="/notes", tags=["Notes"])


router.get("/notes")(get_all_notes)

router.get("/notes/{note_id}")(get_note_by_id)

router.post("/notes")(create_new_note)

router.put("/notes/{note_id}")(update_note)

router.delete("/notes/{note_id}")(delete_note)