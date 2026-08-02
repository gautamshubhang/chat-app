from fastapi import FastAPI
from app.routers import notes

app = FastAPI(
    title="Family Chat API",
    version="0.1.0"
)

app.include_router(notes.router)

