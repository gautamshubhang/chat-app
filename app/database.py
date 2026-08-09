from datetime import datetime
from app.schemas import NoteResponse

# shubhang1234
note_db = {
    1: NoteResponse(id=1, title="Note 1", content="This is the first note", created_at=datetime.now(), updated_at=datetime.now()),
    2: NoteResponse(id=2, title="Note 2", content="This is the second note", created_at=datetime.now(), updated_at=datetime.now())
}