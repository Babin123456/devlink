"""
Tests for the runtime feature flag system.

Evaluation is pure, so most of this exercises ``app/core/feature_flags.py``
directly. The service tests mock ``cache_manager`` -- the flag system must work
with no Redis present, and the tests should not need one either.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from app.core.feature_flags import (
    FLAG_DEFINITIONS,
    FlagDefinition,
    FlagOverride,
    FlagStrategy,
    bucket_for,
    evaluate,
)
from app.services.feature_flag_service import FeatureFlagService

# ----------------------------------------------------------------------
# Definitions
# ----------------------------------------------------------------------


def test_registry_keys_match_their_definitions():
    for key, definition in FLAG_DEFINITIONS.items():
        assert key == definition.key


def test_every_flag_has_a_description():
    for definition in FLAG_DEFINITIONS.values():
        assert definition.description.strip()


def test_percentage_outside_range_is_rejected():
    with pytest.raises(ValueError):
        FlagDefinition(key="bad", description="x", percentage=101)

    with pytest.raises(ValueError):
        FlagDefinition(key="bad", description="x", percentage=-1)


# ----------------------------------------------------------------------
# Bucketing
# ----------------------------------------------------------------------


def test_bucket_is_stable_for_the_same_user_and_flag():
    assert bucket_for("graph_view", "user-1") == bucket_for("graph_view", "user-1")


def test_bucket_is_in_range():
    for index in range(200):
        assert 0 <= bucket_for("graph_view", f"user-{index}") < 100


def test_bucket_differs_across_flags_for_the_same_user():
    # If buckets were keyed on the user alone, the same unlucky cohort would
    # be enrolled in every rollout.
    buckets = {
        bucket_for(flag, "user-1")
        for flag in ("graph_view", "hackathons", "ai_recommendation_panel")
    }
    assert len(buckets) > 1


def test_bucketing_spreads_users_roughly_evenly():
    below_fifty = sum(
        1 for index in range(1000) if bucket_for("graph_view", f"user-{index}") < 50
    )
    # A fair split is 500; allow generous slack so this never flakes.
    assert 400 < below_fifty < 600


# ----------------------------------------------------------------------
# Evaluation
# ----------------------------------------------------------------------


def _flag(**kwargs) -> FlagDefinition:
    return FlagDefinition(key="test_flag", description="test", **kwargs)


def test_on_strategy_is_on_for_everyone():
    definition = _flag(strategy=FlagStrategy.ON)

    assert evaluate(definition, user_id="user-1")
    assert evaluate(definition, user_id=None)


def test_off_strategy_is_off_for_everyone():
    definition = _flag(strategy=FlagStrategy.OFF)

    assert not evaluate(definition, user_id="user-1")
    assert not evaluate(definition, user_id=None)


def test_allowlist_admits_only_listed_users():
    definition = _flag(strategy=FlagStrategy.ALLOWLIST, allowlist=["user-1", "user-2"])

    assert evaluate(definition, user_id="user-1")
    assert evaluate(definition, user_id="user-2")
    assert not evaluate(definition, user_id="user-3")


def test_anonymous_users_never_match_an_allowlist():
    definition = _flag(strategy=FlagStrategy.ALLOWLIST, allowlist=["user-1"])

    assert not evaluate(definition, user_id=None)


def test_anonymous_users_are_off_for_percentage_rollouts():
    definition = _flag(strategy=FlagStrategy.PERCENTAGE, percentage=100)

    assert not evaluate(definition, user_id=None)


def test_zero_percent_is_off_for_everyone():
    definition = _flag(strategy=FlagStrategy.PERCENTAGE, percentage=0)

    assert not any(
        evaluate(definition, user_id=f"user-{index}") for index in range(100)
    )


def test_hundred_percent_is_on_for_every_identified_user():
    definition = _flag(strategy=FlagStrategy.PERCENTAGE, percentage=100)

    assert all(evaluate(definition, user_id=f"user-{index}") for index in range(100))


def test_percentage_rollout_is_stable_across_calls():
    definition = _flag(strategy=FlagStrategy.PERCENTAGE, percentage=50)
    first = [evaluate(definition, user_id=f"user-{i}") for i in range(50)]
    second = [evaluate(definition, user_id=f"user-{i}") for i in range(50)]

    assert first == second


def test_raising_the_percentage_never_removes_a_user():
    # A rollout that took a feature away from someone as it widened would be a
    # nasty surprise; bucketing on a fixed threshold guarantees it cannot.
    users = [f"user-{index}" for index in range(300)]

    enabled_at_25 = {
        user
        for user in users
        if evaluate(_flag(strategy=FlagStrategy.PERCENTAGE, percentage=25), user)
    }
    enabled_at_75 = {
        user
        for user in users
        if evaluate(_flag(strategy=FlagStrategy.PERCENTAGE, percentage=75), user)
    }

    assert enabled_at_25 <= enabled_at_75


def test_allowlisted_user_bypasses_a_zero_percent_rollout():
    definition = _flag(
        strategy=FlagStrategy.PERCENTAGE, percentage=0, allowlist=["user-1"]
    )

    assert evaluate(definition, user_id="user-1")
    assert not evaluate(definition, user_id="user-2")


# ----------------------------------------------------------------------
# Overrides
# ----------------------------------------------------------------------


def test_override_can_force_a_flag_on():
    definition = _flag(strategy=FlagStrategy.OFF)
    override = FlagOverride(strategy=FlagStrategy.ON)

    assert evaluate(definition, user_id="user-1", override=override)


def test_override_can_kill_a_flag():
    definition = _flag(strategy=FlagStrategy.ON)
    override = FlagOverride(strategy=FlagStrategy.OFF)

    assert not evaluate(definition, user_id="user-1", override=override)


def test_override_percentage_alone_keeps_the_definitions_strategy():
    definition = _flag(strategy=FlagStrategy.PERCENTAGE, percentage=0)
    override = FlagOverride(percentage=100)

    assert evaluate(definition, user_id="user-1", override=override)


def test_override_does_not_mutate_the_definition():
    definition = _flag(strategy=FlagStrategy.OFF)
    FlagOverride(strategy=FlagStrategy.ON).apply_to(definition)

    assert definition.strategy is FlagStrategy.OFF


# ----------------------------------------------------------------------
# Service
# ----------------------------------------------------------------------


@pytest.fixture
def service_with_cache():
    """A service whose cache returns nothing unless a test says otherwise."""
    with patch("app.services.feature_flag_service.cache_manager") as cache:
        cache.get.return_value = None
        yield FeatureFlagService(), cache


def test_service_falls_back_to_definitions_without_a_cache(service_with_cache):
    service, _ = service_with_cache

    # graph_view is defined OFF and nothing has overridden it.
    assert service.is_enabled("graph_view", "user-1") is False


def test_unknown_flag_is_disabled_rather_than_raising(service_with_cache):
    service, _ = service_with_cache

    assert service.is_enabled("no_such_flag", "user-1") is False


def test_evaluate_all_covers_every_registered_flag(service_with_cache):
    service, _ = service_with_cache

    assert set(service.evaluate_all("user-1")) == set(FLAG_DEFINITIONS)


def test_stored_override_is_applied(service_with_cache):
    service, cache = service_with_cache
    cache.get.return_value = json.dumps(
        {"strategy": "on", "percentage": None, "allowlist": None}
    )

    assert service.is_enabled("graph_view", "user-1") is True


def test_override_stored_as_a_dict_is_also_accepted(service_with_cache):
    # Redis round-trips give us a string; the in-memory L1 cache hands back
    # whatever was stored. Both shapes have to work.
    service, cache = service_with_cache
    cache.get.return_value = {"strategy": "on"}

    assert service.is_enabled("graph_view", "user-1") is True


def test_malformed_override_is_discarded(service_with_cache):
    service, cache = service_with_cache
    cache.get.return_value = "{not json"

    assert service.is_enabled("graph_view", "user-1") is False


def test_override_with_unknown_strategy_is_discarded(service_with_cache):
    service, cache = service_with_cache
    cache.get.return_value = json.dumps({"strategy": "sometimes"})

    assert service.is_enabled("graph_view", "user-1") is False


def test_override_with_bad_percentage_type_is_discarded(service_with_cache):
    service, cache = service_with_cache
    cache.get.return_value = json.dumps({"strategy": "on", "percentage": "lots"})

    assert service.is_enabled("graph_view", "user-1") is False


def test_cache_failure_falls_back_to_the_definition(service_with_cache):
    service, cache = service_with_cache
    cache.get.side_effect = RuntimeError("redis is down")

    assert service.is_enabled("graph_view", "user-1") is False


def test_set_override_writes_to_the_cache(service_with_cache):
    service, cache = service_with_cache

    assert service.set_override("graph_view", strategy=FlagStrategy.ON) is True

    key, value = cache.set.call_args[0][:2]
    assert key.endswith("graph_view")
    assert json.loads(value)["strategy"] == "on"


def test_set_override_rejects_an_unknown_flag(service_with_cache):
    service, _ = service_with_cache

    with pytest.raises(KeyError):
        service.set_override("no_such_flag", strategy=FlagStrategy.ON)


def test_set_override_rejects_an_out_of_range_percentage(service_with_cache):
    service, _ = service_with_cache

    with pytest.raises(ValueError):
        service.set_override("graph_view", percentage=150)


def test_set_override_reports_failure_when_the_cache_rejects_the_write(
    service_with_cache,
):
    service, cache = service_with_cache
    cache.set.side_effect = RuntimeError("no backend")

    assert service.set_override("graph_view", strategy=FlagStrategy.ON) is False


def test_clear_override_deletes_the_key(service_with_cache):
    service, cache = service_with_cache

    service.clear_override("graph_view")

    assert cache.delete.call_args[0][0].endswith("graph_view")


def test_describe_all_reports_override_state(service_with_cache):
    service, cache = service_with_cache
    cache.get.return_value = json.dumps({"strategy": "on"})

    detail = next(
        item for item in service.describe_all("user-1") if item["key"] == "graph_view"
    )

    assert detail["overridden"] is True
    assert detail["strategy"] == "on"
    assert detail["enabled"] is True


def test_describe_all_reports_no_override_by_default(service_with_cache):
    service, _ = service_with_cache

    detail = next(
        item for item in service.describe_all("user-1") if item["key"] == "graph_view"
    )

    assert detail["overridden"] is False
    assert detail["enabled"] is False


# ----------------------------------------------------------------------
# require_flag dependency
# ----------------------------------------------------------------------


def test_require_flag_returns_404_when_disabled():
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient

    from app.dependencies import get_optional_current_user, require_flag

    app = FastAPI()

    @app.get("/gated", dependencies=[Depends(require_flag("graph_view"))])
    def gated():
        return {"ok": True}

    app.dependency_overrides[get_optional_current_user] = lambda: None

    with patch("app.services.feature_flag_service.cache_manager") as cache:
        cache.get.return_value = None
        response = TestClient(app).get("/gated")

    assert response.status_code == 404


def test_require_flag_allows_through_when_enabled():
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient

    from app.dependencies import get_optional_current_user, require_flag

    app = FastAPI()

    @app.get("/gated", dependencies=[Depends(require_flag("graph_view"))])
    def gated():
        return {"ok": True}

    app.dependency_overrides[get_optional_current_user] = lambda: None

    with patch("app.services.feature_flag_service.cache_manager") as cache:
        cache.get.return_value = json.dumps({"strategy": "on"})
        response = TestClient(app).get("/gated")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_require_flag_evaluates_against_the_calling_user():
    from fastapi import Depends, FastAPI
    from fastapi.testclient import TestClient

    from app.dependencies import get_optional_current_user, require_flag

    app = FastAPI()

    @app.get("/gated", dependencies=[Depends(require_flag("graph_view"))])
    def gated():
        return {"ok": True}

    allowed = MagicMock()
    allowed.id = "user-1"
    app.dependency_overrides[get_optional_current_user] = lambda: allowed

    with patch("app.services.feature_flag_service.cache_manager") as cache:
        cache.get.return_value = json.dumps(
            {"strategy": "allowlist", "allowlist": ["user-1"]}
        )
        assert TestClient(app).get("/gated").status_code == 200

    denied = MagicMock()
    denied.id = "user-9"
    app.dependency_overrides[get_optional_current_user] = lambda: denied

    with patch("app.services.feature_flag_service.cache_manager") as cache:
        cache.get.return_value = json.dumps(
            {"strategy": "allowlist", "allowlist": ["user-1"]}
        )
        assert TestClient(app).get("/gated").status_code == 404
