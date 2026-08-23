from app.schemas import NoteCreate
from app.services.note_service import create_new_note



def test_create_note(db):
    note = NoteCreate(
        title="Test note",
        content="This is a test note"
    )

    result = create_new_note(note, db)

    assert result.title == "Test note"
    assert result.content == "This is a test note"
    assert result.id is not None