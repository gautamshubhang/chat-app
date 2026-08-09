from fastapi import FastAPI
from app.routers import notes
from app.database import engine
from app.model import Note

app = FastAPI(
    title="Family Chat API",
    version="0.1.0"
)

app.include_router(notes.router)

engine.metadata.create_all(engine)

