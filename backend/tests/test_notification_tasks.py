from __future__ import annotations


import uuid

from app.core.celery_app import celery_app
from app.tasks.notification_tasks import send_notification_task
from app.models.notification import Notification, NotificationType
from app.database.base import Base

celery_app.conf.task_always_eager = True
celery_app.conf.task_eager_propagates = True


def test_task_creates_notification():
    import app.tasks.notification_tasks as nt
    from tests.conftest import TestingSessionLocal
    from app.database.session import SessionLocal as RealSessionLocal

    nt.SessionLocal = TestingSessionLocal

    recipient_id = uuid.uuid4()
    sender_id = uuid.uuid4()

    payload = {
        "recipient_id": str(recipient_id),
        "sender_id": str(sender_id),
        "type": NotificationType.FOLLOW.value,
        "title": "New follower",
        "message": "someone followed you",
        "action_url": None,
        "image_url": None,
        "project_id": None,
        "conversation_id": None,
        "message_id": None,
        "application_id": None,
    }

    result = send_notification_task.apply(args=[payload]).get()

    assert result is not None
    db = TestingSessionLocal()
    n = db.get(Notification, uuid.UUID(result))
    assert n is not None
    assert n.type == NotificationType.FOLLOW
    assert n.recipient_id == recipient_id
    assert n.sender_id == sender_id
    db.close()

    nt.SessionLocal = RealSessionLocal


def test_task_skips_self_notification():
    import app.tasks.notification_tasks as nt
    from tests.conftest import TestingSessionLocal
    from app.database.session import SessionLocal as RealSessionLocal

    nt.SessionLocal = TestingSessionLocal

    user_id = uuid.uuid4()

    payload = {
        "recipient_id": str(user_id),
        "sender_id": str(user_id),
        "type": NotificationType.FOLLOW.value,
        "title": "x",
        "message": "y",
        "action_url": None,
        "image_url": None,
        "project_id": None,
        "conversation_id": None,
        "message_id": None,
        "application_id": None,
    }

    result = send_notification_task.apply(args=[payload]).get()
    assert result is None

    nt.SessionLocal = RealSessionLocal


def test_router_enqueue_integration(client):
    import app.tasks.notification_tasks as nt
    from tests.conftest import TestingSessionLocal, engine
    from app.database.session import SessionLocal as RealSessionLocal

    nt.SessionLocal = TestingSessionLocal

    client.post(
        "/api/auth/register",
        json={
            "first_name": "Alice",
            "last_name": "User",
            "email": "alice2@x.com",
            "username": "alice2",
            "password": "Vermilion-Kestrel97!",
        },
    )

    r = client.post(
        "/api/auth/login",
        json={
            "email": "alice2@x.com",
            "password": "Vermilion-Kestrel97!",
        },
    )

    r = client.post(
        "/api/auth/login",
        json={"email": "alice2@x.com", "password": "Vermilion-Kestrel97!"},
    )

    a_tok = r.json()["access_token"]

    a_me = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {a_tok}"},
    )

    print("STATUS:", a_me.status_code)
    print("BODY:", a_me.json())

    a_id = a_me.json()["id"]

    client.post(
        "/api/auth/register",
        json={
            "first_name": "Bob",
            "last_name": "User",
            "email": "bob2@x.com",
            "username": "bob2",
            "password": "Vermilion-Kestrel97!",
        },
    )

    r = client.post(
        "/api/auth/login",
        json={
            "email": "bob2@x.com",
            "password": "Vermilion-Kestrel97!",
        },
    )

    r = client.post(
        "/api/auth/login",
        json={"email": "bob2@x.com", "password": "Vermilion-Kestrel97!"},
    )

    b_tok = r.json()["access_token"]

    r = client.post(
        f"/api/followers/{a_id}", headers={"Authorization": f"Bearer {b_tok}"}
    )
    assert r.status_code == 201

    notifs = client.get(
        "/api/notifications/", headers={"Authorization": f"Bearer {a_tok}"}
    ).json()
    assert any(n["type"] == "follow" for n in notifs)

    nt.SessionLocal = RealSessionLocal
    Base.metadata.drop_all(bind=engine)
