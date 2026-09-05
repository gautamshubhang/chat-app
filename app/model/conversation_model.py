from datetime import datetime
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from app.database import Base

class Conversation(Base):
    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50),nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    memberships = relationship("ConversationMembers", lazy="selectin")

class ConversationMembers(Base):
    __tablename__ = "conversation_members"

    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversation.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    joined_at:  Mapped[datetime] = mapped_column(
        server_default=func.now(),nullable=False)
