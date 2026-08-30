from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
import jwt
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWT_secret(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",extra="ignore")
    jwt_key: str
    jwt_algo: str
    jwt_token_exp_min: int

access_token = JWT_secret()

ph = PasswordHasher()

def hash_password(password: str):
    return ph.hash(password)

def verify_password(password_hash: str, password: str):
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False
    except Exception:
        # Catches other malformed hash errors
        return False  

def create_access_token(id: int):
    SECRET_KEY = access_token.jwt_key
    ALGORITHM = access_token.jwt_algo

    payload = {
        "sub": str(id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=access_token.jwt_token_exp_min),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str):
    SECRET_KEY = access_token.jwt_key
    ALGORITHM = access_token.jwt_algo
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Session has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid Token")