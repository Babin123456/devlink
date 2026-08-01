from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.tech_stack import TechStackRequest
from app.services.ai_service import AIService


def _client() -> TestClient:
    client = TestClient(app)
    client.app.state.limiter.enabled = False
    return client


def test_recommend_tech_stack_endpoint_returns_ranked_recommendations():
    """POST /recommendations/tech-stack returns ranked recommendations with explanations."""
    client = _client()
    r = client.post(
        "/recommendations/tech-stack",
        json={"project_idea": "Food Delivery Platform"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["project_idea"] == "Food Delivery Platform"
    assert len(body["recommendations"]) > 0
    for rec in body["recommendations"]:
        assert rec["name"]
        assert rec["category"]
        assert rec["reason"]
        assert 0.0 <= rec["confidence"] <= 1.0
    assert body["summary"]


def test_recommend_tech_stack_domain_fallback():
    """Fallback stack matches the project idea domain."""
    client = _client()
    r = client.post(
        "/recommendations/tech-stack",
        json={"project_idea": "Food Delivery Platform"},
    )
    names = {rec["name"] for rec in r.json()["recommendations"]}
    assert "React" in names
    assert "PostgreSQL" in names


def test_recommend_tech_stack_rejects_short_idea():
    """project_idea shorter than 3 characters is rejected by validation."""
    client = _client()
    r = client.post("/recommendations/tech-stack", json={"project_idea": "ab"})
    assert r.status_code == 422


def test_recommend_tech_stack_service_fallback_without_api_key(monkeypatch):
    """Service falls back to rule-based recommendations when no OpenAI key is set."""
    monkeypatch.setattr("app.services.ai_service.settings.OPENAI_API_KEY", "")
    response = AIService.recommend_tech_stack(
        TechStackRequest(project_idea="AI analytics dashboard")
    )
    names = [rec.name for rec in response.recommendations]
    assert "Python" in names
    assert all(0.0 <= rec.confidence <= 1.0 for rec in response.recommendations)
