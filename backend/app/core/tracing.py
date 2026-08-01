from contextvars import ContextVar
from typing import Optional

correlation_id_ctx: ContextVar[Optional[str]] = ContextVar(
    "correlation_id_ctx", default=None
)
request_id_ctx: ContextVar[Optional[str]] = ContextVar("request_id_ctx", default=None)


def get_correlation_id() -> Optional[str]:
    """Retrieve current correlation ID from contextvar."""
    return correlation_id_ctx.get()


def get_request_id() -> Optional[str]:
    """Retrieve current request ID from contextvar."""
    return request_id_ctx.get()


def set_correlation_id(cid: str) -> None:
    """Set current correlation ID in contextvar."""
    correlation_id_ctx.set(cid)
    request_id_ctx.set(cid)
