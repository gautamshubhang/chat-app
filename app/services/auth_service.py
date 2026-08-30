from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import create_access_token, decode_access_token, verify_password
from app.schemas.user_schemas import TokenResponse, UserLogin, UserRegister
from app.repositories.user_repository import get_user_by_username, get_user_by_email, get_user_by_id, add_user
from app.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_new_user(user_data: UserRegister, db: Session):
    if get_user_by_username(user_data.username, db):
        raise ValueError("Username already taken")
    elif get_user_by_email(user_data.email, db):
        raise ValueError("Email already used")

    return add_user(user_data, db)


def user_login(user_data: UserLogin, db: Session):
    rsp = get_user_by_username(user_data.username, db)

    # login happens only if verify password is true, else throws error
    if not rsp:
        raise ValueError("Username or Password incorrect")
    elif verify_password(rsp.password_hash, user_data.password):
        token = create_access_token(rsp.id)
        return TokenResponse(access_token=token, token_type="Bearer")
    else:
        raise ValueError("Username or Password incorrect")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        user = get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
