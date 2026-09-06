from sqlalchemy.orm import Session, selectinload
from app.model.conversation_model import Conversation, ConversationMembers
from app.model.user_model import User
from app.repositories.message_repository import add_member_by_id, create_conversation_with_members
from app.schemas.conversation_schemas import ConversationResponse, CreateConversation, MemberAdd
from sqlalchemy import func, insert, select



def create_new_conversation(data: CreateConversation, db: Session, current_user: User) -> ConversationResponse:

    unique_member_ids = set(data.members)
    unique_member_ids.add(current_user.id)

    existing_users_count = db.execute(select(func.count(User.id)).where(User.id.in_(unique_member_ids))).scalar()
    
    if existing_users_count != len(unique_member_ids):
        raise ValueError(f"Incorrect User Ids provided")

    new_conversation = CreateConversation(
        name = data.name,
        members = list(unique_member_ids)
    )

    result = create_conversation_with_members(new_conversation,current_user.id,db)

    return result

def get_all_conversation(db: Session, current_user: User) -> list[ConversationResponse]:
    stmt = (
        select(Conversation)
        .join(ConversationMembers, Conversation.id == ConversationMembers.conversation_id)
        .where(ConversationMembers.user_id == current_user.id)
        .options(selectinload(Conversation.memberships))
    )
    
    conversations = db.execute(stmt).scalars().all()
    
    return [
        ConversationResponse(
            id=c.id,
            name=c.name,
            created_at=c.created_at,
            members=[m.user_id for m in c.memberships]
        )
        for c in conversations
    ]
      

def get_conversation_by_id(db: Session, current_user: User, conversation_id: int) -> ConversationResponse:
    stmt = (
        select(Conversation)
        .join(ConversationMembers, Conversation.id == ConversationMembers.conversation_id)
        .where(
            ConversationMembers.user_id == current_user.id, 
            ConversationMembers.conversation_id == conversation_id
        )
        .options(selectinload(Conversation.memberships))
    )
    conversation = db.execute(stmt).scalars().first()

    if not conversation:
        raise ValueError("Conversation not found or unauthorized")

    return ConversationResponse(
        id=conversation.id,
        name=conversation.name,
        created_at=conversation.created_at,
        members=[m.user_id for m in conversation.memberships]
    )

def add_new_conversation_members(conversation_id: int, data: MemberAdd, db: Session, current_user: User) -> ConversationResponse:
    incoming_ids = set(data.member_id)

    stmt = (
        select(Conversation)
        .where(
            Conversation.created_by == current_user.id, 
            Conversation.id == conversation_id
        )
        .options(selectinload(Conversation.memberships))
    )
    conversation = db.execute(stmt).scalars().first()
    
    if not conversation:
        raise ValueError("Conversation not found")

    existing_member_ids = {m.user_id for m in conversation.memberships}
    
    existing_users_count = db.execute(
        select(func.count(User.id)).where(User.id.in_(incoming_ids))
    ).scalar()
    
    if existing_users_count != len(incoming_ids):
        raise ValueError("One or more provided User IDs do not exist")

    new_ids_to_add = incoming_ids - existing_member_ids
    # If all provided users are already in the chat, just return the current room state
    if new_ids_to_add:
        result = add_member_by_id(new_ids_to_add,conversation,db)
        return result

    return ConversationResponse(
        id=conversation.id,
        name=conversation.name,
        created_at=conversation.created_at,
        members=[m.user_id for m in conversation.memberships]
    )
        