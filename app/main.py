from fastapi import FastAPI
from app.routers import notes
from app.database import engine, Base
from app.model import Note

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Family Chat API",
    version="0.1.0"
)

app.include_router(notes.router)

