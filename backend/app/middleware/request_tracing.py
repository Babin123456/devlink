import time
import uuid
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings
from app.core.logging import log_request
from app.core.tracing import correlation_id_ctx, request_id_ctx


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that manages request correlation IDs for end-to-end distributed tracing.

    - Extracts incoming correlation ID from X-Correlation-ID, X-Request-ID, or X-Trace-ID headers.
    - Generates a unique UUID4 trace ID if no incoming header is provided.
    - Stores correlation ID in request state, async ContextVar, and structlog context.
    - Attaches X-Correlation-ID and X-Request-ID headers to outgoing responses.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Check incoming tracing headers
        correlation_id = (
            request.headers.get("X-Correlation-ID")
            or request.headers.get("X-Request-ID")
            or request.headers.get("X-Trace-ID")
        )

        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Set request state
        request.state.correlation_id = correlation_id
        request.state.request_id = correlation_id

        # Set async ContextVar tokens
        token_cid = correlation_id_ctx.set(correlation_id)
        token_rid = request_id_ctx.set(correlation_id)

        # Bind structlog contextvars for current async context
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            correlation_id=correlation_id,
            request_id=correlation_id,
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000

            log_request(
                request_id=correlation_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
            )

            # Attach tracing response headers
            response.headers[settings.CORRELATION_ID_HEADER] = correlation_id
            response.headers[settings.REQUEST_ID_HEADER] = correlation_id

            return response
        finally:
            correlation_id_ctx.reset(token_cid)
            request_id_ctx.reset(token_rid)
            structlog.contextvars.clear_contextvars()
