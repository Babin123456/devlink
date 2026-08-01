from __future__ import annotations

import pytest
from app.core.config import settings
from app.middleware.rate_limit import (
    COMMENT_LIMIT,
    LOGIN_LIMIT,
    MESSAGE_LIMIT,
    PASSWORD_RESET_LIMIT,
    REGISTER_LIMIT,
    SEARCH_LIMIT,
    limiter,
)


def test_rate_limit_settings_defined():
    """Verify rate limit setting variables are defined in application config."""
    assert settings.LOGIN_RATE_LIMIT == "5/minute"
    assert settings.REGISTER_RATE_LIMIT == "3/hour"
    assert settings.PASSWORD_RESET_RATE_LIMIT == "3/15minutes"
    assert settings.MESSAGE_RATE_LIMIT == "30/minute"
    assert settings.COMMENT_RATE_LIMIT == "30/minute"
    assert settings.SEARCH_RATE_LIMIT == "60/minute"


def test_rate_limit_constants_exported():
    """Verify exported rate limit constants exist and are usable by routers."""
    assert LOGIN_LIMIT is not None
    assert REGISTER_LIMIT is not None
    assert PASSWORD_RESET_LIMIT is not None
    assert MESSAGE_LIMIT is not None
    assert COMMENT_LIMIT is not None
    assert SEARCH_LIMIT is not None


def test_limiter_instance_configured():
    """Verify global Limiter instance is initialized."""
    assert limiter is not None
