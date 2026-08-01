from app.middleware.request_tracing import RequestTracingMiddleware


class RequestIDMiddleware(RequestTracingMiddleware):
    """
    Backward-compatible RequestIDMiddleware inheriting from RequestTracingMiddleware.

    Provides unique Request ID and Correlation ID tracing across services.
    """

    pass
