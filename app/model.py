from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50),nullable=False)
    content: Mapped[str] = mapped_column(String(500),nullable=False)
    created_at: Mapped[datetime] = mapped_column(
            server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False)
    is_pinned: Mapped[bool] = mapped_column(default=False,nullable=False)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    password_hash: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    created_at: Mapped[datetime] = mapped_column(
                server_default=func.now(),nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
                server_default=func.now(),
                onupdate=func.now(),
                nullable=False)
