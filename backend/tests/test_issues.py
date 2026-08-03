from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.issue import DuplicateSuggestion, Issue, IssueStatus
from app.models.project import Project, ProjectStage, ProjectVisibility
from app.models.user import User
from app.services.duplicate_detection_service import DuplicateDetectionService
from app.services.issue_service import IssueService


@pytest.fixture
def no_openai(monkeypatch):
    """Force the keyword-based fallback by disabling embedding generation."""
    monkeypatch.setattr(
        "app.services.issue_service.DuplicateDetectionService.generate_embedding",
        staticmethod(lambda text: None),
    )
    monkeypatch.setattr(
        DuplicateDetectionService,
        "generate_embedding",
        staticmethod(lambda text: None),
    )


@pytest.fixture
def issue_project(db: Session):
    owner = User(
        id=uuid.uuid4(),
        email="issues_owner@example.com",
        username="issues_owner",
        first_name="Issues",
        last_name="Owner",
        password_hash="hashed_password",
        is_active=True,
    )
    project = Project(
        id=uuid.uuid4(),
        owner_id=owner.id,
        title="Issues Test Project",
        slug="issues-test-project",
        description="Testing issue tracking",
        stage=ProjectStage.MVP,
        visibility=ProjectVisibility.PUBLIC,
        views=0,
    )
    db.add_all([owner, project])
    db.commit()
    db.refresh(owner)
    db.refresh(project)
    return owner, project


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_create_issue(
    client: TestClient, register_and_login, issue_project, db: Session
):
    _, project = issue_project
    user_id, token = register_and_login("issues_create@example.com", "issues_create")

    response = client.post(
        f"/api/projects/{project.id}/issues",
        json={
            "title": "App crashes on startup",
            "description": "The app crashes immediately after launch on macOS.",
            "priority": "high",
            "labels": "bug, crash",
        },
        headers=_auth_headers(token),
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "App crashes on startup"
    assert data["project_id"] == str(project.id)
    assert data["author_id"] == user_id
    assert data["status"] == "open"


def test_create_issue_rejects_empty_title(
    client: TestClient, register_and_login, issue_project
):
    _, project = issue_project
    _, token = register_and_login("issues_bad_title@example.com", "issues_bad_title")

    response = client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "", "description": "Some description"},
        headers=_auth_headers(token),
    )

    assert response.status_code == 422


def test_list_issues(client: TestClient, register_and_login, issue_project):
    _, project = issue_project
    _, token = register_and_login("issues_list@example.com", "issues_list")
    headers = _auth_headers(token)

    for i in range(3):
        client.post(
            f"/api/projects/{project.id}/issues",
            json={"title": f"Issue number {i}", "description": f"Description {i}"},
            headers=headers,
        )

    response = client.get(f"/api/projects/{project.id}/issues", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_issue_returns_duplicate_suggestions(
    client: TestClient, register_and_login, issue_project, db: Session
):
    _, project = issue_project
    user_id, token = register_and_login("issues_get@example.com", "issues_get")

    created = client.post(
        f"/api/projects/{project.id}/issues",
        json={
            "title": "Button not responding",
            "description": "Clicking does nothing.",
        },
        headers=_auth_headers(token),
    ).json()

    response = client.get(
        f"/api/projects/{project.id}/issues/{created['id']}",
        headers=_auth_headers(token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]
    assert "duplicate_suggestions" in data
    assert data["author"]["username"] == "issues_get"


def test_update_issue(client: TestClient, register_and_login, issue_project):
    _, project = issue_project
    _, token = register_and_login("issues_update@example.com", "issues_update")
    headers = _auth_headers(token)

    created = client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "Old title", "description": "Old description"},
        headers=headers,
    ).json()

    response = client.put(
        f"/api/projects/{project.id}/issues/{created['id']}",
        json={"title": "New title", "status": "in_progress"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "in_progress"


def test_delete_issue(client: TestClient, register_and_login, issue_project):
    _, project = issue_project
    _, token = register_and_login("issues_delete@example.com", "issues_delete")
    headers = _auth_headers(token)

    created = client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "To delete", "description": "Remove me"},
        headers=headers,
    ).json()

    response = client.delete(
        f"/api/projects/{project.id}/issues/{created['id']}", headers=headers
    )

    assert response.status_code == 204

    listing = client.get(f"/api/projects/{project.id}/issues", headers=headers).json()
    assert listing == []


def test_check_duplicates_keyword_fallback(
    client: TestClient, register_and_login, issue_project, db: Session, no_openai
):
    _, project = issue_project
    _, token = register_and_login("issues_dup@example.com", "issues_dup")
    headers = _auth_headers(token)

    client.post(
        f"/api/projects/{project.id}/issues",
        json={
            "title": "Login button crashes the app",
            "description": "Clicking login crashes the whole application.",
        },
        headers=headers,
    )

    response = client.post(
        f"/api/projects/{project.id}/issues/check-duplicates",
        json={
            "title": "Login button crashes the app",
            "description": "Clicking login crashes the whole application.",
        },
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["has_duplicates"] is True
    assert len(data["suggestions"]) >= 1
    assert data["suggestions"][0]["similarity_score"] >= 0.75
    assert data["suggestions"][0]["issue"]["title"] == "Login button crashes the app"
    assert data["checked_count"] >= 1

    # Transient results must NOT be persisted to the database
    persisted = db.scalar(select(func.count()).select_from(DuplicateSuggestion))
    assert persisted == 0


def test_check_duplicates_no_match(
    client: TestClient, register_and_login, issue_project, db: Session, no_openai
):
    _, project = issue_project
    _, token = register_and_login("issues_nodup@example.com", "issues_nodup")
    headers = _auth_headers(token)

    client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "Fix typo in readme", "description": "One character typo."},
        headers=headers,
    )

    response = client.post(
        f"/api/projects/{project.id}/issues/check-duplicates",
        json={
            "title": "Add kubernetes autoscaling docs",
            "description": "Document horizontal pod autoscaling configuration.",
        },
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["has_duplicates"] is False
    assert data["suggestions"] == []


def test_mark_as_duplicate(
    client: TestClient, register_and_login, issue_project, db: Session
):
    _, project = issue_project
    _, token = register_and_login("issues_mark@example.com", "issues_mark")
    headers = _auth_headers(token)

    original = client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "Original bug report", "description": "Original description."},
        headers=headers,
    ).json()

    duplicate = client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "Same bug reported again", "description": "Duplicate report."},
        headers=headers,
    ).json()

    response = client.post(
        f"/api/projects/{project.id}/issues/{duplicate['id']}/mark-duplicate/{original['id']}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "duplicate"

    # Relationship is persisted for the marked issue
    suggestion = db.scalar(
        select(DuplicateSuggestion).where(
            DuplicateSuggestion.source_issue_id == uuid.UUID(duplicate["id"]),
            DuplicateSuggestion.duplicate_issue_id == uuid.UUID(original["id"]),
        )
    )
    assert suggestion is not None
    assert suggestion.similarity_score == 1.0


def test_mark_as_duplicate_requires_author(
    client: TestClient, register_and_login, issue_project
):
    _, project = issue_project
    user_id, token = register_and_login("issues_mark2@example.com", "issues_mark2")
    _, other_token = register_and_login("issues_mark3@example.com", "issues_mark3")

    created = client.post(
        f"/api/projects/{project.id}/issues",
        json={"title": "Someone else's issue", "description": "Not mine."},
        headers=_auth_headers(token),
    ).json()

    response = client.post(
        f"/api/projects/{project.id}/issues/{created['id']}/mark-duplicate/{created['id']}",
        headers=_auth_headers(other_token),
    )

    assert response.status_code == 403


def test_issue_service_check_duplicates_does_not_persist(
    db: Session, issue_project, no_openai
):
    _, project = issue_project
    owner, _ = issue_project

    db.add_all(
        [
            Issue(
                project_id=project.id,
                author_id=owner.id,
                title="Service level duplicate",
                description="First report of this problem.",
            )
        ]
    )
    db.flush()

    from app.schemas.issue import DuplicateCheckRequest

    result = IssueService.check_duplicates(
        db,
        project.id,
        DuplicateCheckRequest(
            title="Service level duplicate",
            description="First report of this problem.",
        ),
    )

    assert result.has_duplicates is True

    persisted = db.scalar(select(func.count()).select_from(DuplicateSuggestion))
    assert persisted == 0
