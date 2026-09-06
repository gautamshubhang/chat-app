from sqlalchemy import insert
from sqlalchemy.orm import Session
from app.model.conversation_model import Conversation, ConversationMembers
from app.model.message_model import Message
from app.schemas.conversation_schemas import ConversationResponse, CreateConversation
from app.schemas.message_schemas import ReceiveMessage


def create_conversation_with_members(data: CreateConversation, creator: int, db: Session) -> ConversationResponse:
    conversation = Conversation(
        name=data.name,
        created_by=creator
        )
    db.add(conversation)
    db.flush()

    member_mappings = [
        {"conversation_id": conversation.id, "user_id": uid} 
        for uid in data.members
    ]
    db.execute(insert(ConversationMembers), member_mappings)
    db.commit()
    db.refresh(conversation)
    return ConversationResponse(
        id=conversation.id, 
        name=conversation.name, 
        created_at=conversation.created_at, 
        members=[m.user_id for m in conversation.memberships]
    )

def send_message(message:Message, db:Session) -> ReceiveMessage:
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return ReceiveMessage(id=message.id,sender_id=message.sender_id, content=message.content, created_at=message.created_at)

def add_member_by_id(new_ids_to_add: set, conversation: Conversation, db:Session) -> ConversationResponse:
    new_mappings = [
                {"conversation_id": conversation.id, "user_id": uid} 
                for uid in new_ids_to_add
            ]
    db.execute(insert(ConversationMembers), new_mappings)
    db.commit()
    db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        name=conversation.name,
        created_at=conversation.created_at,
        members=[m.user_id for m in conversation.memberships]
    )