from datetime import datetime
from pydantic import BaseModel, field_validator

class CreateConversation(BaseModel):
    name: str
    members: list[int]

    @field_validator('name')
    @classmethod

    def name_validation(cls, value: str) -> str:
        if not value:
            raise ValueError("Name must be provided")
        elif len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        else:
            return value

    @field_validator('members')
    @classmethod

    def member_list_validation(cls, value: list[int]) -> list[int]:
        if not value or len(value) < 2:
            raise ValueError("Atleast 2 members need to be added")
        else:
            return value

class MemberAdd(BaseModel):
    member_id: list[int]

    @field_validator('member_id')
    @classmethod

    def name_validation(cls, value: list[int]) -> list[int]:
        if not value:
            raise ValueError("Member Id not provided")
        else:
            return value


class ConversationResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    members: list[int]