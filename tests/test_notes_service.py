from app.schemas import NoteCreate
from app.services.note_service import create_new_note, get_all_notes, get_note_by_id, update_note, delete_note
from pydantic import ValidationError
import pytest


def test_create_note(db):
    note = NoteCreate(
        title="Test note",
        content="This is a test note"
    )

    result = create_new_note(note, db)

    assert result.title == "Test note"
    assert result.content == "This is a test note"
    assert result.id is not None

def test_create_note_with_empty_title():
    with pytest.raises(ValidationError) as exc:
        NoteCreate(title="", content="This is a test note")
    assert "Title must be provided" in str(exc.value)

def test_create_note_with_empty_content():
    with pytest.raises(ValidationError) as exc:
        NoteCreate(title="Test", content = "")
    assert "Content must be provided" in str(exc.value)

def test_create_note_with_long_title():
    with pytest.raises(ValidationError) as exc:
        NoteCreate(
        title="T" * 51,
        content="This is a test note")
    assert "Title must not exceed 50 characters" in str(exc.value)

def test_create_note_with_long_content():
    with pytest.raises(ValidationError) as exc:
        NoteCreate(
            title="Test note",
            content="C" * 501
        )
    assert "Content must not exceed 500 characters" in str(exc.value)