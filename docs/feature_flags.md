# Feature Flags

DevLink has two kinds of switch.

The `ENABLE_*` booleans in `app/core/config.py` are **build-time** switches:
changing one means editing the environment and restarting the process. They are
right for "does this deployment have email configured at all".

This document covers the **runtime** layer added in #856: flags that can be
flipped without a deploy, targeted at a subset of users, and rolled out
gradually. They are right for "is the graph view ready for everyone yet".

> This is first-party toggling. It is unrelated to the third-party
> extensibility discussed in #582.

## Why

Without this, incomplete work either sits on a long-lived branch or gets merged
with the route commented out, and a misbehaving feature cannot be turned off
without shipping a release.

## Defining a flag

Flags live in `FLAG_DEFINITIONS` in `app/core/feature_flags.py`:

```python
FlagDefinition(
    key="graph_view",
    description="Interactive collaboration graph on /graph.",
    strategy=FlagStrategy.OFF,
)
```

Adding an entry is all that is needed — it appears in the API and can be used
with `require_flag()` immediately. **Define new flags as `OFF`.** A flag
somebody forgot to configure should stay dark.

## Strategies

| Strategy     | Behaviour                                                      |
| :----------- | :------------------------------------------------------------- |
| `on`         | On for everyone, including anonymous callers.                   |
| `off`        | Off for everyone. The kill switch.                              |
| `percentage` | On for a stable percentage of identified users.                 |
| `allowlist`  | On only for an explicit list of user ids.                       |

### Percentage rollouts

Users are bucketed by `sha256("<flag_key>:<user_id>")`, which gives three
properties that matter:

- **Stable.** A user's bucket never changes, so a feature cannot flicker on and
  off between requests. (This is why the built-in `hash()` is not used — it is
  salted per process, so two workers would disagree.)
- **Independent per flag.** The flag key is part of the hash, so the same
  unlucky cohort does not get enrolled in every rollout.
- **Monotonic.** Raising the percentage only ever adds users. Widening a
  rollout never takes the feature away from someone who already had it.

Users on the `allowlist` are always in, whatever the percentage — so the team
can dogfood something still sitting at 0%.

Anonymous callers cannot be bucketed, so a `percentage` or `allowlist` flag is
off for them.

## Using a flag

### Gating a route

```python
from app.dependencies import require_flag

@router.get("/graph", dependencies=[Depends(require_flag("graph_view"))])
def collaboration_graph(...):
    ...
```

A disabled flag yields **404, not 403**. A 403 confirms the route exists and
merely refuses you, which leaks the shape of unreleased work; a 404 is
indistinguishable from the route not being deployed.

### Checking in code

```python
from app.services.feature_flag_service import feature_flag_service

if feature_flag_service.is_enabled("duplicate_project_detection", str(user.id)):
    ...
```

An unknown key returns `False` and logs a warning. A typo should leave a
feature dark, not take down the endpoint checking it.

### From the frontend

`GET /api/feature-flags` returns the whole evaluated map in one request:

```json
{
  "flags": {
    "graph_view": false,
    "hackathons": false,
    "ai_recommendation_panel": true,
    "design_system_route": false,
    "duplicate_project_detection": false
  }
}
```

The endpoint is open to anonymous callers, because the landing page needs to
know what to render before anyone has logged in.

## Runtime overrides

Overrides are stored in Redis via the existing cache manager and take
precedence over the definition. Fields left unset fall through, so bumping a
percentage does not mean restating the strategy.

Administrator endpoints:

| Method   | Path                             | Purpose                             |
| :------- | :------------------------------- | :---------------------------------- |
| `GET`    | `/api/admin/feature-flags`       | All flags with strategy and state   |
| `PUT`    | `/api/admin/feature-flags/{key}` | Apply an override                   |
| `DELETE` | `/api/admin/feature-flags/{key}` | Clear it, reverting to the definition |

```http
PUT /api/admin/feature-flags/ai_recommendation_panel
Authorization: Bearer <admin_token>

{ "percentage": 25 }
```

Overrides expire after seven days. That is long enough to be effectively
permanent for an incident kill switch, while stopping forgotten experiments
from lingering forever.

### No Redis?

Everything works without it — flags simply resolve to their definitions, which
is what local development and CI want. Writing an override in that state
returns **503** rather than reporting a success that would evaporate on the
next request.

A malformed or unreadable override is discarded with a warning and the
definition is used. Bad cache contents must not break every request that
evaluates the flag.

## Removing a flag

Flags are temporary. Once a feature is on for everyone and has stayed that way,
delete the entry from `FLAG_DEFINITIONS` and drop the `require_flag` guard. A
registry full of permanently-on flags is just dead branching.
