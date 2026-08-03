import datetime
from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.activity_response import ActivityResponse
from ...models.activity_type import ActivityType
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 50,
    cursor: datetime.datetime | None | Unset = UNSET,
    actor_id: None | Unset | UUID = UNSET,
    target_id: None | Unset | UUID = UNSET,
    target_type: None | str | Unset = UNSET,
    activity_types: list[ActivityType] | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    elif isinstance(cursor, datetime.datetime):
        json_cursor = cursor.isoformat()
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    json_actor_id: None | str | Unset
    if isinstance(actor_id, Unset):
        json_actor_id = UNSET
    elif isinstance(actor_id, UUID):
        json_actor_id = str(actor_id)
    else:
        json_actor_id = actor_id
    params["actor_id"] = json_actor_id

    json_target_id: None | str | Unset
    if isinstance(target_id, Unset):
        json_target_id = UNSET
    elif isinstance(target_id, UUID):
        json_target_id = str(target_id)
    else:
        json_target_id = target_id
    params["target_id"] = json_target_id

    json_target_type: None | str | Unset
    if isinstance(target_type, Unset):
        json_target_type = UNSET
    else:
        json_target_type = target_type
    params["target_type"] = json_target_type

    json_activity_types: list[str] | None | Unset
    if isinstance(activity_types, Unset):
        json_activity_types = UNSET
    elif isinstance(activity_types, list):
        json_activity_types = []
        for activity_types_type_0_item_data in activity_types:
            activity_types_type_0_item = activity_types_type_0_item_data.value
            json_activity_types.append(activity_types_type_0_item)

    else:
        json_activity_types = activity_types
    params["activity_types"] = json_activity_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/activities/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ActivityResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ActivityResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | list[ActivityResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: datetime.datetime | None | Unset = UNSET,
    actor_id: None | Unset | UUID = UNSET,
    target_id: None | Unset | UUID = UNSET,
    target_type: None | str | Unset = UNSET,
    activity_types: list[ActivityType] | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[ActivityResponse]]:
    """Get Feed

    Args:
        limit (int | Unset):  Default: 50.
        cursor (datetime.datetime | None | Unset): Cursor for pagination (created_at timestamp)
        actor_id (None | Unset | UUID): Filter by actor
        target_id (None | Unset | UUID): Filter by target
        target_type (None | str | Unset): Filter by target type
        activity_types (list[ActivityType] | None | Unset): Filter by activity types

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ActivityResponse]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        actor_id=actor_id,
        target_id=target_id,
        target_type=target_type,
        activity_types=activity_types,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: datetime.datetime | None | Unset = UNSET,
    actor_id: None | Unset | UUID = UNSET,
    target_id: None | Unset | UUID = UNSET,
    target_type: None | str | Unset = UNSET,
    activity_types: list[ActivityType] | None | Unset = UNSET,
) -> HTTPValidationError | list[ActivityResponse] | None:
    """Get Feed

    Args:
        limit (int | Unset):  Default: 50.
        cursor (datetime.datetime | None | Unset): Cursor for pagination (created_at timestamp)
        actor_id (None | Unset | UUID): Filter by actor
        target_id (None | Unset | UUID): Filter by target
        target_type (None | str | Unset): Filter by target type
        activity_types (list[ActivityType] | None | Unset): Filter by activity types

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ActivityResponse]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        cursor=cursor,
        actor_id=actor_id,
        target_id=target_id,
        target_type=target_type,
        activity_types=activity_types,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: datetime.datetime | None | Unset = UNSET,
    actor_id: None | Unset | UUID = UNSET,
    target_id: None | Unset | UUID = UNSET,
    target_type: None | str | Unset = UNSET,
    activity_types: list[ActivityType] | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[ActivityResponse]]:
    """Get Feed

    Args:
        limit (int | Unset):  Default: 50.
        cursor (datetime.datetime | None | Unset): Cursor for pagination (created_at timestamp)
        actor_id (None | Unset | UUID): Filter by actor
        target_id (None | Unset | UUID): Filter by target
        target_type (None | str | Unset): Filter by target type
        activity_types (list[ActivityType] | None | Unset): Filter by activity types

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ActivityResponse]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        cursor=cursor,
        actor_id=actor_id,
        target_id=target_id,
        target_type=target_type,
        activity_types=activity_types,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 50,
    cursor: datetime.datetime | None | Unset = UNSET,
    actor_id: None | Unset | UUID = UNSET,
    target_id: None | Unset | UUID = UNSET,
    target_type: None | str | Unset = UNSET,
    activity_types: list[ActivityType] | None | Unset = UNSET,
) -> HTTPValidationError | list[ActivityResponse] | None:
    """Get Feed

    Args:
        limit (int | Unset):  Default: 50.
        cursor (datetime.datetime | None | Unset): Cursor for pagination (created_at timestamp)
        actor_id (None | Unset | UUID): Filter by actor
        target_id (None | Unset | UUID): Filter by target
        target_type (None | str | Unset): Filter by target type
        activity_types (list[ActivityType] | None | Unset): Filter by activity types

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ActivityResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            cursor=cursor,
            actor_id=actor_id,
            target_id=target_id,
            target_type=target_type,
            activity_types=activity_types,
        )
    ).parsed
