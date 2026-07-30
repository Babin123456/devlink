from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.refresh_token import RefreshToken
from app.models.user import User


@pytest.fixture
def session_users(db: Session):
    user1 = User(
        id=uuid.uuid4(),
        email="session_user1@example.com",
        username="session_user1",
        first_name="Session",
        last_name="User1",
        password_hash="hashed_password",
        is_active=True,
    )
    user2 = User(
        id=uuid.uuid4(),
        email="session_user2@example.com",
        username="session_user2",
        first_name="Session",
        last_name="User2",
        password_hash="hashed_password",
        is_active=True,
    )
    db.add_all([user1, user2])
    db.commit()
    return user1, user2


@pytest.fixture
def user_tokens(db: Session, session_users):
    user1, user2 = session_users
    now = datetime.now(timezone.utc)
    expires = now + timedelta(days=7)

    # 3 active tokens for User 1
    t1 = RefreshToken(
        id=uuid.uuid4(),
        user_id=user1.id,
        token="token_user1_session1",
        device_name="Desktop Chrome",
        is_revoked=False,
        expires_at=expires,
    )
    t2 = RefreshToken(
        id=uuid.uuid4(),
        user_id=user1.id,
        token="token_user1_session2",
        device_name="Mobile Safari",
        is_revoked=False,
        expires_at=expires,
    )
    t3 = RefreshToken(
        id=uuid.uuid4(),
        user_id=user1.id,
        token="token_user1_session3",
        device_name="Tablet Firefox",
        is_revoked=False,
        expires_at=expires,
    )
    # 1 token for User 2
    t4 = RefreshToken(
        id=uuid.uuid4(),
        user_id=user2.id,
        token="token_user2_session1",
        device_name="User2 Laptop",
        is_revoked=False,
        expires_at=expires,
    )

    db.add_all([t1, t2, t3, t4])
    db.commit()
    return t1, t2, t3, t4


def test_list_active_sessions(client: TestClient, session_users, user_tokens):
    user1, _ = session_users
    t1, _, _, _ = user_tokens
    access_token = create_access_token(str(user1.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    res = client.get(f"/api/auth/sessions?current_session_id={t1.id}", headers=headers)
    assert res.status_code == 200
    sessions = res.json()
    assert len(sessions) == 3

    # Verify is_current flag for t1
    curr = [s for s in sessions if s["id"] == str(t1.id)]
    assert len(curr) == 1
    assert curr[0]["is_current"] is True


def test_revoke_individual_session(client: TestClient, session_users, user_tokens):
    user1, _ = session_users
    t1, t2, _, _ = user_tokens
    access_token = create_access_token(str(user1.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Revoke session t2
    res = client.delete(f"/api/auth/sessions/{t2.id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["success"] is True

    # List active sessions should now have 2 active sessions
    res = client.get("/api/auth/sessions", headers=headers)
    assert res.status_code == 200
    sessions = res.json()
    assert len(sessions) == 2
    session_ids = [s["id"] for s in sessions]
    assert str(t2.id) not in session_ids


def test_revoke_other_sessions(client: TestClient, session_users, user_tokens):
    user1, _ = session_users
    t1, t2, t3, _ = user_tokens
    access_token = create_access_token(str(user1.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Revoke all except t1
    res = client.post(
        f"/api/auth/sessions/revoke-others?current_session_id={t1.id}", headers=headers
    )
    assert res.status_code == 200
    assert res.json()["revoked_count"] == 2

    # List active sessions should now only contain t1
    res = client.get("/api/auth/sessions", headers=headers)
    assert res.status_code == 200
    sessions = res.json()
    assert len(sessions) == 1
    assert sessions[0]["id"] == str(t1.id)


def test_revoke_session_not_found(client: TestClient, session_users, user_tokens):
    user1, _ = session_users
    _, _, _, t4 = user_tokens
    access_token = create_access_token(str(user1.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Try revoking non-existent session
    res = client.delete(f"/api/auth/sessions/{uuid.uuid4()}", headers=headers)
    assert res.status_code == 404

    # Try revoking user2's session using user1 credentials
    res = client.delete(f"/api/auth/sessions/{t4.id}", headers=headers)
    assert res.status_code == 404
