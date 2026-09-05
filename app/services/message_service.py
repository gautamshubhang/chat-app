from sqlalchemy.orm import Session
from sqlalchemy import select
from app.model.message_model import Message
from app.model.conversation_model import ConversationMembers
from app.schemas.message_schemas import SendMessage, RecieveMessage
from app.model.user_model import User


def create_message(conversation_id: int, message: SendMessage, db: Session, current_user: User) -> RecieveMessage:
    # verify user is a member of the conversation
    stmt = select(ConversationMembers).where(
        ConversationMembers.conversation_id == conversation_id,
        ConversationMembers.user_id == current_user.id,
    )
    membership = db.execute(stmt).scalars().first()
    if not membership:
        raise ValueError("Conversation not found or unauthorized")

    new_message = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=message.content,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return RecieveMessage(sender_id=new_message.sender_id, content=new_message.content, created_at=new_message.created_at)


def get_messages(conversation_id: int, db: Session, current_user: User) -> list[RecieveMessage]:
    # verify membership
    stmt = select(ConversationMembers).where(
        ConversationMembers.conversation_id == conversation_id,
        ConversationMembers.user_id == current_user.id,
    )
    membership = db.execute(stmt).scalars().first()
    if not membership:
        raise ValueError("Conversation not found or unauthorized")

    stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    msgs = db.execute(stmt).scalars().all()

    return [RecieveMessage(sender_id=m.sender_id, content=m.content, created_at=m.created_at) for m in msgs]
