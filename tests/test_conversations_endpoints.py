from typing import Tuple


def register_user(client, username: str, password: str, email: str) -> dict:
    r = client.post("/auth/register", json={"username": username, "password": password, "email": email})
    assert r.status_code == 200
    return r.json()


def login_user(client, username: str, password: str) -> Tuple[str, dict]:
    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    token = r.json().get("access_token")
    return token, r.json()


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_authenticated_user_can_create_conversation(client):
    u1 = register_user(client, "c_user1", "Password1!", "c1@example.com")
    u2 = register_user(client, "c_user2", "Password1!", "c2@example.com")
    u3 = register_user(client, "c_user3", "Password1!", "c3@example.com")

    token, _ = login_user(client, "c_user1", "Password1!")

    payload = {"name": "room1", "members": [u2["id"], u3["id"]]}
    r = client.post("/conversations/", json=payload, headers=auth_headers(token))
    assert r.status_code == 200
    resp = r.json()
    assert set(resp["members"]) == {u1["id"], u2["id"], u3["id"]}


def test_unauthenticated_user_cannot_create_conversation(client):
    # attempt without auth
    r = client.post("/conversations/", json={"name": "roomx", "members": [1,2]})
    assert r.status_code == 401


def test_creator_automatically_becomes_member(client):
    u1 = register_user(client, "cm_user1", "Password1!", "cm1@example.com")
    u2 = register_user(client, "cm_user2", "Password1!", "cm2@example.com")

    token, _ = login_user(client, "cm_user1", "Password1!")
    r = client.post("/conversations/", json={"name": "roomcm", "members": [u2["id"], u1["id"]]}, headers=auth_headers(token))
    assert r.status_code == 200
    resp = r.json()
    assert u1["id"] in resp["members"]


def test_user_can_list_their_conversations_and_cannot_see_others(client):
    # create users and conversation between a and b
    ua = register_user(client, "list_a", "Password1!", "la@example.com")
    ub = register_user(client, "list_b", "Password1!", "lb@example.com")
    uc = register_user(client, "list_c", "Password1!", "lc@example.com")

    token_a, _ = login_user(client, "list_a", "Password1!")
    r = client.post("/conversations/", json={"name":"listroom","members":[ub["id"], ua["id"]]}, headers=auth_headers(token_a))
    assert r.status_code == 200
    conv = r.json()

    # b should see it
    token_b, _ = login_user(client, "list_b", "Password1!")
    r = client.get("/conversations/", headers=auth_headers(token_b))
    assert any(c["id"] == conv["id"] for c in r.json())

    # c should NOT see it
    token_c, _ = login_user(client, "list_c", "Password1!")
    r = client.get("/conversations/", headers=auth_headers(token_c))
    assert all(c["id"] != conv["id"] for c in r.json())


def test_creator_can_add_member_and_noncreator_cannot_and_cannot_add_nonexistent_or_duplicate(client):
    # setup users
    creator = register_user(client, "add_creator", "Password1!", "ac@example.com")
    member = register_user(client, "add_member", "Password1!", "am@example.com")
    new_member = register_user(client, "add_new", "Password1!", "an@example.com")
    outsider = register_user(client, "add_out", "Password1!", "ao@example.com")

    token_creator, _ = login_user(client, "add_creator", "Password1!")
    token_member, _ = login_user(client, "add_member", "Password1!")

    # create conversation with creator + member
    r = client.post("/conversations/", json={"name":"addroom","members":[member["id"], creator["id"]]}, headers=auth_headers(token_creator))
    assert r.status_code == 200
    conv = r.json()

    # creator can add new_member
    r = client.post(f"/conversations/{conv['id']}/members", json={"member_id":[new_member["id"]]}, headers=auth_headers(token_creator))
    assert r.status_code == 200
    resp = r.json()
    assert new_member["id"] in resp["members"]

    # non-creator (member) cannot add outsider
    r = client.post(f"/conversations/{conv['id']}/members", json={"member_id":[outsider["id"]]}, headers=auth_headers(token_member))
    assert r.status_code == 403

    # cannot add nonexistent user
    r = client.post(f"/conversations/{conv['id']}/members", json={"member_id":[999999]}, headers=auth_headers(token_creator))
    assert r.status_code == 403

    # cannot add same user twice (no duplicate in members)
    before = set(resp["members"])
    r = client.post(f"/conversations/{conv['id']}/members", json={"member_id":[new_member["id"]]}, headers=auth_headers(token_creator))
    assert r.status_code == 200
    after = set(r.json()["members"])
    assert before == after


def test_messages_member_send_and_retrieve_and_access_control_and_order(client):
    # users
    u1 = register_user(client, "m_user1", "Password1!", "mu1@example.com")
    u2 = register_user(client, "m_user2", "Password1!", "mu2@example.com")
    u3 = register_user(client, "m_user3", "Password1!", "mu3@example.com")

    t1, _ = login_user(client, "m_user1", "Password1!")
    t2, _ = login_user(client, "m_user2", "Password1!")
    t3, _ = login_user(client, "m_user3", "Password1!")

    # create conversation between u1 and u2
    r = client.post("/conversations/", json={"name":"mroom","members":[u2["id"], u1["id"]]}, headers=auth_headers(t1))
    assert r.status_code == 200
    conv = r.json()

    # member (u2) can send message
    r = client.post(f"/conversations/{conv['id']}/messages", json={"content":"hello from u2"}, headers=auth_headers(t2))
    assert r.status_code == 200
    msg = r.json()
    assert msg["sender_id"] == u2["id"]
    assert msg["content"] == "hello from u2"

    # non-member (u3) cannot send
    r = client.post(f"/conversations/{conv['id']}/messages", json={"content":"i should not"}, headers=auth_headers(t3))
    assert r.status_code == 400

    # sender automatically comes from JWT (already validated above)

    # member can retrieve messages
    r = client.get(f"/conversations/{conv['id']}/messages", headers=auth_headers(t1))
    assert r.status_code == 200
    msgs = r.json()
    assert any(m["content"] == "hello from u2" for m in msgs)

    # non-member cannot retrieve
    r = client.get(f"/conversations/{conv['id']}/messages", headers=auth_headers(t3))
    assert r.status_code == 404

    # messages returned chronologically
    # send two messages in order
    client.post(f"/conversations/{conv['id']}/messages", json={"content":"first"}, headers=auth_headers(t1))
    client.post(f"/conversations/{conv['id']}/messages", json={"content":"second"}, headers=auth_headers(t2))
    r = client.get(f"/conversations/{conv['id']}/messages", headers=auth_headers(t1))
    assert r.status_code == 200
    texts = [m["content"] for m in r.json()]
    # ensure 'first' comes before 'second'
    assert texts.index("first") < texts.index("second")
