from datetime import datetime
from pydantic import BaseModel, field_validator

class NotesResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class NotesCreate(BaseModel):
    title: str
    content: str

    @field_validator('title')
    @classmethod

    def validate_title(cls, value: str) -> str:
        if value is None or len(value) < 1:
            raise ValueError("Title must be provided")
        elif len(value) > 50:
            raise ValueError("Title must not exceed 50 characters")
        return value

    @field_validator('content')
    @classmethod

    def validate_content(cls, value: str) -> str:
        if value is None or len(value) < 1:
            raise ValueError("Content must be provided")
        elif len(value) > 500:
            raise ValueError("Content must not exceed 500 characters")
        return value

class NotesUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

    @field_validator('title')
    @classmethod

    def validate_title(cls, value: str):
        if value is None or len(value) < 1:
            return None
        elif len(value) > 50:
            raise ValueError("Title must not exceed 50 characters")
        return value

    @field_validator('content')
    @classmethod

    def validate_content(cls, value: str):
        if value is None or len(value) < 1:
            return None
        elif len(value) > 500:
            raise ValueError("Content must not exceed 500 characters")
        return value
