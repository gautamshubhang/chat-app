from datetime import datetime
import string
from pydantic import BaseModel, field_validator, EmailStr


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

    @field_validator('username')
    @classmethod

    def username_validation(cls, value: str) -> str:
        if not value:
            raise ValueError("Name must be provided")
        elif len(value) > 20:
            raise ValueError("Name must not exceed 20 characters")
        elif len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value

    @field_validator('password')
    @classmethod

    def password_validation(cls, value: str) -> str:
        if not value:
            raise ValueError("Password must be provided")
        elif len(value) > 50:
            raise ValueError("Password must not exceed 50 characters")
        elif len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        elif not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        elif not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        elif not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one Digit")
        elif not any(char in string.punctuation for char in value):
            raise ValueError("Password must contain at least one special character")
        elif any(char.isspace() for char in value):
            raise ValueError("Password must not contain space")
        return value

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not value:
            raise ValueError("Email must be provided")
        elif len(value) > 255:
            raise ValueError("Email must not exceed 255 characters")
        return value


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime