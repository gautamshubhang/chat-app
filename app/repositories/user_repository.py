from sqlalchemy import select
from app.model import User
from argon2 import PasswordHasher
from app.schemas.user_schemas import UserRegister, UserResponse
from sqlalchemy.orm import Session


def add_user(user_data:UserRegister, db: Session):
    ph = PasswordHasher()
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash = ph.hash(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserResponse(id=new_user.id, username=new_user.username, email=new_user.email, created_at=new_user.created_at)

def get_user_by_username(username, db: Session):
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalars().first()

def get_user_by_email(email, db: Session):
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalars().first()