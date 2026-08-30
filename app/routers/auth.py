from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.model import User
from app.schemas.user_schemas import TokenResponse, UserLogin, UserRegister, UserResponse
from app.services.auth_service import create_new_user, get_current_user, user_login


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register",response_model=UserResponse)
def create_new_user_endpoint(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        return create_new_user(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login",response_model=TokenResponse)
def user_login_endpoint(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        return user_login(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, username=current_user.username, email=current_user.email, created_at=current_user.created_at)
