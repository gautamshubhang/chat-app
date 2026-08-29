from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserRegister
from app.repositories.user_repository import get_user_by_username,get_user_by_email,add_user


def create_new_user(user_data: UserRegister, db: Session):
    if get_user_by_username(user_data.username, db):
        raise ValueError("Username already taken")
    elif get_user_by_email(user_data.email,db):
        raise ValueError("Email already used")
    
    return add_user(user_data,db)
    