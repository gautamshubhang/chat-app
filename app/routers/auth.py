from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.schemas.user_schemas import UserRegister, UserResponse
from app.services.auth_service import create_new_user


router = APIRouter(prefix="/users", tags=["Auth"])

@router.post("/",response_model=UserResponse)
def create_new_user_endpoint(user_data, db: Session = Depends(get_db)):
    try:
        return create_new_user(user_data, db)
    except ValueError as e:
        if str(e) in ("Username already taken","Email already used"):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    
