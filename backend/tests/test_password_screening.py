"""
Tests for compromised-password screening.

Covers the offline blocklist, the personal-information check, and the Have I
Been Pwned range lookup. The HIBP transport is always mocked -- the suite must
not depend on a third party being reachable.
"""

import hashlib
from unittest.mock import patch

import httpx
import pytest
from fastapi import HTTPException

from app.core.password_blocklist import (
    COMMON_PASSWORDS,
    contains_personal_information,
    is_common_password,
    normalise_password,
)
from app.services.password_breach_service import PasswordBreachService
from app.utils.validators import validate_password


# ----------------------------------------------------------------------
# Normalisation
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("password", "password"),
        ("PASSWORD", "password"),
        ("P@ssw0rd", "password"),
        ("p@$$w0rd", "password"),
        ("Password2025!", "password"),
        ("Welcome123", "welcome"),
    ],
)
def test_normalise_password_folds_to_the_core_word(raw, expected):
    assert normalise_password(raw) == expected


def test_normalisation_never_yields_an_empty_blocklist_entry():
    # A purely numeric entry folds away to "". If that leaked into the
    # blocklist every password whose core folds away would be rejected.
    assert "" not in COMMON_PASSWORDS


# ----------------------------------------------------------------------
# Blocklist
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "password",
    [
        "password",
        "Password",
        "PASSWORD",
        "P@ssw0rd",
        "Password1!",
        "Welcome123!",
        "Qwerty123",
        "Admin123!",
        "Letmein123",
        "Devlink123!",
        "Summer2025!",
        "Changeme123",
    ],
)
def test_common_passwords_are_recognised(password):
    assert is_common_password(password)


@pytest.mark.parametrize(
    "password",
    [
        "correct-horse-battery-staple",
        "Tr0ub4dor&3xkcd",
        "vermilion-kestrel-97",
        "QuietLoomBaseline#8",
    ],
)
def test_unusual_passwords_are_not_flagged(password):
    assert not is_common_password(password)


def test_empty_password_is_not_flagged_as_common():
    assert not is_common_password("")


# ----------------------------------------------------------------------
# Personal information
# ----------------------------------------------------------------------


def test_password_containing_username_is_rejected():
    assert contains_personal_information(
        "AlexRivera2025!", username="alexrivera"
    )


def test_password_containing_email_local_part_is_rejected():
    assert contains_personal_information(
        "Rivera#2025", email="rivera@devlink.app"
    )


def test_dotted_username_is_split_into_tokens():
    assert contains_personal_information("Rivera!99", username="alex.rivera")


def test_email_domain_alone_does_not_trigger():
    # Everyone shares the domain, so matching on it would reject far too much.
    assert not contains_personal_information(
        "QuietLoom#8421", email="alex@devlink.app"
    )


def test_short_tokens_are_ignored():
    # A two-letter username would otherwise match almost any password.
    assert not contains_personal_information("QuietLoom#8421", username="al")


def test_unrelated_password_passes_the_context_check():
    assert not contains_personal_information(
        "vermilion-kestrel-97",
        username="alexrivera",
        email="alex@devlink.app",
    )


# ----------------------------------------------------------------------
# HIBP range lookup
# ----------------------------------------------------------------------


def _range_body_for(password: str, count: int) -> str:
    """Build a realistic range response containing the given password."""
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    suffix = digest[5:]
    return "\n".join(
        [
            "0000000000000000000000000000000000A:0",
            f"{suffix}:{count}",
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:12",
        ]
    )


def _response(status_code: int, text: str = "") -> httpx.Response:
    """
    Build a response with its request attached.

    ``raise_for_status`` needs the originating request, so a bare
    ``httpx.Response(200, text=...)`` blows up inside the service.
    """
    return httpx.Response(
        status_code,
        text=text,
        request=httpx.Request("GET", "https://hibp.test/range/ABCDE"),
    )


@pytest.fixture
def breach_service():
    service = PasswordBreachService(api_url="https://hibp.test/range", timeout=1.0)
    with patch("app.services.password_breach_service.cache_manager") as cache:
        cache.get.return_value = None
        yield service


def _enable_hibp(monkeypatch):
    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "ENABLE_HIBP_CHECK", True)


def test_only_the_hash_prefix_is_sent(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)
    password = "vermilion-kestrel-97"
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(200, _range_body_for(password, 42))
        breach_service.breach_count(password)

    requested_url = mock_get.call_args[0][0]

    assert requested_url.endswith(f"/{digest[:5]}")
    # Neither the password nor the rest of its digest may appear anywhere in
    # the outbound request.
    assert password not in requested_url
    assert digest[5:] not in requested_url


def test_padding_is_requested(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(200, "ABC:1")
        breach_service.breach_count("vermilion-kestrel-97")

    assert mock_get.call_args.kwargs["headers"]["Add-Padding"] == "true"


def test_breach_count_returns_the_matching_count(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)
    password = "vermilion-kestrel-97"

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(200, _range_body_for(password, 4213))
        assert breach_service.breach_count(password) == 4213


def test_absent_suffix_counts_as_zero(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(
            200, "0000000000000000000000000000000000A:0"
        )
        assert breach_service.breach_count("vermilion-kestrel-97") == 0


def test_is_compromised_respects_the_minimum_count(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)

    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "HIBP_MIN_BREACH_COUNT", 5)
    password = "vermilion-kestrel-97"

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(200, _range_body_for(password, 2))
        assert not breach_service.is_compromised(password)

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(200, _range_body_for(password, 900))
        assert breach_service.is_compromised(password)


def test_network_failure_fails_open(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)

    with patch("httpx.get", side_effect=httpx.ConnectTimeout("timed out")):
        assert breach_service.breach_count("vermilion-kestrel-97") == 0
        assert not breach_service.is_compromised("vermilion-kestrel-97")


def test_server_error_fails_open(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(503)
        assert breach_service.breach_count("vermilion-kestrel-97") == 0


def test_malformed_count_is_treated_as_zero(monkeypatch, breach_service):
    _enable_hibp(monkeypatch)
    digest = hashlib.sha1(b"vermilion-kestrel-97").hexdigest().upper()

    with patch("httpx.get") as mock_get:
        mock_get.return_value = _response(200, f"{digest[5:]}:not-a-number")
        assert breach_service.breach_count("vermilion-kestrel-97") == 0


def test_disabled_check_skips_the_network_entirely(monkeypatch, breach_service):
    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "ENABLE_HIBP_CHECK", False)

    with patch("httpx.get") as mock_get:
        assert breach_service.breach_count("password") == 0

    mock_get.assert_not_called()


def test_cached_range_is_reused(monkeypatch):
    _enable_hibp(monkeypatch)
    password = "vermilion-kestrel-97"
    service = PasswordBreachService(api_url="https://hibp.test/range")

    with patch("app.services.password_breach_service.cache_manager") as cache:
        cache.get.return_value = _range_body_for(password, 77)

        with patch("httpx.get") as mock_get:
            assert service.breach_count(password) == 77

        mock_get.assert_not_called()


# ----------------------------------------------------------------------
# validate_password integration
# ----------------------------------------------------------------------


def test_composition_rules_still_apply():
    # The screening layer is additive: the original length and character-class
    # rules must still fire first.
    with pytest.raises(HTTPException) as exc:
        validate_password("Ab1!")

    assert exc.value.status_code == 400
    assert "at least 8 characters" in exc.value.detail


def test_strong_unique_password_is_accepted():
    assert (
        validate_password(
            "vermilion-Kestrel-97!",
            username="alexrivera",
            email="alex@devlink.app",
        )
        == "vermilion-Kestrel-97!"
    )


def test_common_password_is_rejected_by_validate_password():
    with pytest.raises(HTTPException) as exc:
        validate_password("Password123!")

    assert exc.value.status_code == 400
    assert "too common" in exc.value.detail


def test_password_containing_username_is_rejected_by_validate_password():
    with pytest.raises(HTTPException) as exc:
        validate_password("AlexRivera#2025", username="alexrivera")

    assert exc.value.status_code == 400
    assert "username or email" in exc.value.detail


def test_error_message_does_not_echo_the_password():
    with pytest.raises(HTTPException) as exc:
        validate_password("Password123!")

    assert "Password123!" not in exc.value.detail


def test_blocklist_can_be_disabled(monkeypatch):
    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "ENABLE_PASSWORD_BLOCKLIST", False)
    monkeypatch.setattr(config_module.settings, "ENABLE_HIBP_CHECK", False)

    assert validate_password("Password123!") == "Password123!"


def test_breached_password_is_rejected_by_validate_password(monkeypatch):
    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "ENABLE_HIBP_CHECK", True)
    password = "vermilion-Kestrel-97!"

    with patch("app.services.password_breach_service.cache_manager") as cache:
        cache.get.return_value = _range_body_for(password, 5000)

        with pytest.raises(HTTPException) as exc:
            validate_password(password)

    assert "known data breach" in exc.value.detail


def test_hibp_outage_does_not_block_registration(monkeypatch):
    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "ENABLE_HIBP_CHECK", True)

    with patch("app.services.password_breach_service.cache_manager") as cache:
        cache.get.return_value = None
        with patch("httpx.get", side_effect=httpx.ConnectError("no route")):
            assert (
                validate_password("vermilion-Kestrel-97!")
                == "vermilion-Kestrel-97!"
            )
