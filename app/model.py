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

