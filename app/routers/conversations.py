from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.model.user_model import User
from app.schemas.conversation_schemas import ConversationResponse, CreateConversation, MemberAdd
from app.schemas.message_schemas import RecieveMessage, SendMessage
from app.services.auth_service import get_current_user
from app.services.conversation_service import add_new_conversation_members, create_new_conversation, get_all_conversation, get_conversation_by_id
from app.services.message_service import create_message, get_messages


router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/",response_model=ConversationResponse)
def create_new_conversation_endpoint(data: CreateConversation, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_new_conversation(data,db,current_user)
    except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/",response_model=list[ConversationResponse])
def get_all_conversation_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_all_conversation(db,current_user)
    except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{conversation_id}",response_model=ConversationResponse)
def get_conversation_by_id_endpoint(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_conversation_by_id(db,current_user,conversation_id)
    except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{conversation_id}/members",response_model=ConversationResponse)
def create_new_conversation_endpoint(conversation_id: int, member_id: MemberAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return add_new_conversation_members(conversation_id,member_id,db,current_user)
    except ValueError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/{conversation_id}/messages", response_model=RecieveMessage)
def post_message_endpoint(conversation_id: int, message: SendMessage, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_message(conversation_id, message, db, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{conversation_id}/messages", response_model=list[RecieveMessage])
def get_messages_endpoint(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_messages(conversation_id, db, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

