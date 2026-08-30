from app.core.security import create_access_token, access_token
import jwt
from app.core.security import decode_access_token
import pytest


# --- Login tests ---

def test_login_valid_username_password(client):
    # register
    payload = {"username": "loginuser", "password": "Password1!", "email": "login@example.com"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200

    # login
    r = client.post("/auth/login", json={"username": "loginuser", "password": "Password1!"})
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data.get("token_type") == "Bearer"


def test_login_wrong_password(client):
    payload = {"username": "wpuser", "password": "Password1!", "email": "wp@example.com"}
    client.post("/auth/register", json=payload)

    r = client.post("/auth/login", json={"username": "wpuser", "password": "WrongPass1!"})
    assert r.status_code == 401


def test_login_nonexistent_username(client):
    r = client.post("/auth/login", json={"username": "noone", "password": "Password1!"})
    assert r.status_code == 401


# --- JWT tests ---

def test_jwt_valid_token_decoded():
    # create a token for subject 1
    token = create_access_token(1)
    payload = decode_access_token(token)
    assert payload.get("sub") is not None


def test_jwt_tampered_token_401(client):
    payload = {"username": "tuser", "password": "Password1!", "email": "tuser@example.com"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/login", json={"username": "tuser", "password": "Password1!"})
    token = r.json().get("access_token")
    tampered = token + "a"

    headers = {"Authorization": f"Bearer {tampered}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 401


def test_jwt_expired_token_401(client):
    # temporarily set expiry to negative minutes to force expiration
    original = access_token.jwt_token_exp_min
    access_token.jwt_token_exp_min = -1
    token = create_access_token(999)
    access_token.jwt_token_exp_min = original

    # decoding directly raises ValueError (expired)
    with pytest.raises(ValueError):
        decode_access_token(token)

    # and using endpoint returns 401
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 401


def test_jwt_missing_sub_401(client):
    # craft a token without sub
    key = access_token.jwt_key
    algo = access_token.jwt_algo
    token = jwt.encode({"foo": "bar"}, key, algorithm=algo)

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 401


# --- /auth/me tests ---

def test_no_authorization_header_401(client):
    r = client.get("/auth/me")
    assert r.status_code == 401


def test_malformed_authorization_header_401(client):
    headers = {"Authorization": "BadHeader"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 401


def test_invalid_token_401(client):
    headers = {"Authorization": "Bearer totally.invalid.token"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 401


def test_valid_token_returns_user(client):
    payload = {"username": "meuser", "password": "Password1!", "email": "me@example.com"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/login", json={"username": "meuser", "password": "Password1!"})
    token = r.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data.get("username") == "meuser"
    assert data.get("email") == "me@example.com"


# --- Integration test: register -> login -> me ---

def test_register_login_getme_integration(client):
    payload = {"username": "flowuser", "password": "Password1!", "email": "flow@example.com"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 200
    user = r.json()

    r = client.post("/auth/login", json={"username": "flowuser", "password": "Password1!"})
    assert r.status_code == 200
    token = r.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 200
    me = r.json()
    assert me.get("username") == user.get("username")
    assert me.get("email") == user.get("email")
