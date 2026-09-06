from datetime import datetime
from pydantic import BaseModel, field_validator

class SendMessage(BaseModel):
    content: str
    
    @field_validator('content')
    @classmethod

    def name_validation(cls, value: str) -> str:
        if not value:
            raise ValueError("Content must be provided")
        elif len(value) > 5000:
            raise ValueError("Message must not contain more than 5000 characters")
        else:
            return value

class ReceiveMessage(BaseModel):
    id: int
    sender_id: int
    content: str
    created_at: datetime