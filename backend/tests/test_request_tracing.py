import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.tracing import get_correlation_id, get_request_id
from app.middleware.request_tracing import RequestTracingMiddleware


@pytest.fixture
def tracing_app():
    test_app = FastAPI()
    test_app.add_middleware(RequestTracingMiddleware)

    @test_app.get("/test-tracing")
    async def sample_endpoint():
        return {
            "status": "ok",
            "correlation_id": get_correlation_id(),
            "request_id": get_request_id(),
        }

    return test_app


@pytest.fixture
def client(tracing_app):
    return TestClient(tracing_app)


def test_request_tracing_generates_correlation_id(client):
    """
    Test that a unique UUID4 correlation ID is generated when none is provided.
    """
    response = client.get("/api/test-tracing")
    assert response.status_code == 200

    headers = response.headers
    assert "X-Correlation-ID" in headers
    assert "X-Request-ID" in headers
    assert headers["X-Correlation-ID"] == headers["X-Request-ID"]

    body = response.json()
    assert body["correlation_id"] == headers["X-Correlation-ID"]
    assert body["request_id"] == headers["X-Request-ID"]
    assert len(body["correlation_id"]) == 36  # UUID length


def test_request_tracing_preserves_incoming_correlation_id(client):
    """
    Test that an incoming X-Correlation-ID header is preserved and propagated.
    """
    incoming_id = "trace-custom-correlation-12345"
    response = client.get(
        "/test-tracing",
        headers={"X-Correlation-ID": incoming_id},
    )

    assert response.status_code == 200
    headers = response.headers

    assert headers["X-Correlation-ID"] == incoming_id
    assert headers["X-Request-ID"] == incoming_id

    body = response.json()
    assert body["correlation_id"] == incoming_id
    assert body["request_id"] == incoming_id


def test_request_tracing_preserves_incoming_request_id(client):
    """
    Test that an incoming X-Request-ID header is preserved as the correlation ID.
    """
    incoming_id = "req-service-header-67890"
    response = client.get(
        "/test-tracing",
        headers={"X-Request-ID": incoming_id},
    )

    assert response.status_code == 200
    headers = response.headers

    assert headers["X-Correlation-ID"] == incoming_id
    assert headers["X-Request-ID"] == incoming_id

    body = response.json()
    assert body["correlation_id"] == incoming_id


def test_request_tracing_preserves_incoming_trace_id(client):
    """
    Test that an incoming X-Trace-ID header is preserved when other headers are absent.
    """
    incoming_id = "opentelemetry-trace-abcde"
    response = client.get(
        "/test-tracing",
        headers={"X-Trace-ID": incoming_id},
    )

    assert response.status_code == 200
    headers = response.headers

    assert headers["X-Correlation-ID"] == incoming_id
    assert headers["X-Request-ID"] == incoming_id

    body = response.json()
    assert body["correlation_id"] == incoming_id
