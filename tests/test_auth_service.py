from app.schemas.user_schemas import UserRegister
from app.services.auth_service import create_new_user
from app.model import User
from sqlalchemy import select
import pytest
from argon2 import PasswordHasher


def test_register_valid_user(db):
    user = UserRegister(username="testuser", password="Password1!", email="test1@gmail.com")
    resp = create_new_user(user, db)
    assert resp.username == "testuser"

    stmt = select(User).where(User.username == "testuser")
    user_db = db.execute(stmt).scalars().first()
    assert user_db is not None
    assert user_db.email == "test1@gmail.com"
    assert hasattr(user_db, "password_hash")
    assert user_db.password_hash != "Password1!"
    ph = PasswordHasher()
    assert ph.verify(user_db.password_hash, "Password1!")


def test_duplicate_username(db):
    user1 = UserRegister(username="dupuser", password="Password1!", email="dup1@example.com")
    create_new_user(user1, db)

    user2 = UserRegister(username="dupuser", password="Password2@", email="dup2@example.com")
    with pytest.raises(ValueError) as exc:
        create_new_user(user2, db)
    assert "Username already taken" in str(exc.value)


def test_duplicate_email(db):
    user1 = UserRegister(username="uniquser", password="Password1!", email="dupemail@example.com")
    create_new_user(user1, db)

    user2 = UserRegister(username="anotheruser", password="Password2@", email="dupemail@example.com")
    with pytest.raises(ValueError) as exc:
        create_new_user(user2, db)
    assert "Email already used" in str(exc.value)


def test_plain_password_not_stored(db):
    user = UserRegister(username="plainuser", password="Password1!", email="plain@example.com")
    create_new_user(user, db)

    stmt = select(User).where(User.username == "plainuser")
    user_db = db.execute(stmt).scalars().first()
    assert user_db is not None
    # model should not have a plain `password` attribute or column
    assert not hasattr(user_db, "password")
    assert "password" not in [c.name for c in User.__table__.columns]
    assert user_db.password_hash != "Password1!"
