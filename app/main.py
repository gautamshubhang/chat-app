from fastapi import FastAPI
from app.routers import notes, auth, conversations



app = FastAPI(
    title="Family Chat API",
    version="0.1.0"
)

app.include_router(notes.router)
app.include_router(auth.router)
app.include_router(conversations.router)

