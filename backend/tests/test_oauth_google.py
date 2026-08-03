import pytest
from app.models.user import User
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def override_google_config(monkeypatch):
    monkeypatch.setattr("app.core.config.settings.GOOGLE_CLIENT_ID", "test_client_id")
    monkeypatch.setattr("app.core.config.settings.GOOGLE_CLIENT_SECRET", "test_client_secret")
    monkeypatch.setattr("app.core.config.settings.GOOGLE_REDIRECT_URI", "http://localhost:5173/auth/google/callback")


def test_google_login_success_new_user(client: TestClient, db, override_google_config):
    # Mock token exchange
    mock_post = AsyncMock()
    mock_response_token = MagicMock()
    mock_response_token.status_code = 200
    mock_response_token.json.return_value = {"access_token": "mocked_google_token"}
    mock_post.return_value = mock_response_token

    # Mock user profile from Google API
    mock_get = AsyncMock()
    mock_response_user = MagicMock()
    mock_response_user.status_code = 200
    mock_response_user.json.return_value = {
        "id": "google_id_12345",
        "email": "googleuser@example.com",
        "given_name": "Google",
        "family_name": "User",
        "picture": "https://google.com/avatar.png",
    }
    mock_get.return_value = mock_response_user

    with patch("httpx.AsyncClient.post", new=mock_post):
        with patch("httpx.AsyncClient.get", new=mock_get):
            with patch("app.routers.auth.oauth_redis.get", new_callable=AsyncMock) as mock_redis_get:
                mock_redis_get.return_value = "1"
                with patch("app.routers.auth.oauth_redis.delete", new_callable=AsyncMock):
                    response = client.post("/api/auth/google", json={"code": "test_code_123", "state": "test_state"})

                    assert response.status_code == 200
                    data = response.json()
                    assert "access_token" in data
                    assert data["user"]["email"] == "googleuser@example.com"
                    assert data["user"]["first_name"] == "Google"
                    
                    # Verify DB state
                    user = db.query(User).filter(User.email == "googleuser@example.com").first()
                    assert user is not None
                    assert user.google_id == "google_id_12345"
                    assert user.is_verified is True


def test_google_login_link_existing_account(client: TestClient, db, override_google_config):
    # Pre-create a user with the same email but no google_id
    from app.core.security import hash_password

    existing_user = User(
        first_name="Existing",
        last_name="User",
        username="google_existing",
        email="googleexisting@example.com",
        password_hash=hash_password("Password123!"),
        is_active=True,
    )
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)

    mock_post = AsyncMock()
    mock_response_token = MagicMock()
    mock_response_token.status_code = 200
    mock_response_token.json.return_value = {"access_token": "mocked_google_token"}
    mock_post.return_value = mock_response_token

    mock_get = AsyncMock()
    mock_response_user = MagicMock()
    mock_response_user.status_code = 200
    mock_response_user.json.return_value = {
        "id": "google_id_67890",
        "email": "googleexisting@example.com",
        "given_name": "Existing",
        "family_name": "User",
    }
    mock_get.return_value = mock_response_user

    with patch("httpx.AsyncClient.post", new=mock_post):
        with patch("httpx.AsyncClient.get", new=mock_get):
            with patch("app.routers.auth.oauth_redis.get", new_callable=AsyncMock) as mock_redis_get:
                mock_redis_get.return_value = "1"
                with patch("app.routers.auth.oauth_redis.delete", new_callable=AsyncMock):
                    response = client.post("/api/auth/google", json={"code": "test_code_456", "state": "valid_state"})

                    assert response.status_code == 200
                    data = response.json()
                    assert data["user"]["email"] == "googleexisting@example.com"
                    assert data["user"]["username"] == "google_existing"

                    # Verify DB state
                    db.expire_all()
                    user = db.query(User).filter(User.email == "googleexisting@example.com").first()
                    assert user.google_id == "google_id_67890"


def test_google_login_invalid_code(client: TestClient, override_google_config):
    mock_post = AsyncMock()
    mock_response_token = MagicMock()
    mock_response_token.status_code = 400
    mock_response_token.json.return_value = {
        "error": "invalid_grant",
        "error_description": "The provided code is invalid.",
    }
    mock_post.return_value = mock_response_token

    with patch("httpx.AsyncClient.post", new=mock_post):
        with patch("app.routers.auth.oauth_redis.get", new_callable=AsyncMock) as mock_redis_get:
            mock_redis_get.return_value = "1"
            with patch("app.routers.auth.oauth_redis.delete", new_callable=AsyncMock):
                response = client.post("/api/auth/google", json={"code": "invalid_code", "state": "test_state"})
                assert response.status_code == 401
                assert "invalid" in response.json()["detail"].lower()


def test_google_login_invalid_state(client: TestClient, override_google_config):
    with patch("app.routers.auth.oauth_redis.get", new_callable=AsyncMock) as mock_redis_get:
        # State not found in redis
        mock_redis_get.return_value = None
        response = client.post("/api/auth/google", json={"code": "some_code", "state": "invalid_state"})
        assert response.status_code == 400
        assert "Invalid or expired OAuth state" in response.json()["detail"]
