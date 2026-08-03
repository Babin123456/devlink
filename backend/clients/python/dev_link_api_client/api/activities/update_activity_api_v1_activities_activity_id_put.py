from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.activity_response import ActivityResponse
from ...models.activity_update import ActivityUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    activity_id: UUID,
    *,
    body: ActivityUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/activities/{activity_id}".format(
            activity_id=quote(str(activity_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ActivityResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = ActivityResponse.from_dict(response.json())

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
) -> Response[ActivityResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    activity_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ActivityUpdate,
) -> Response[ActivityResponse | HTTPValidationError]:
    """Update Activity

    Args:
        activity_id (UUID):
        body (ActivityUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActivityResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        activity_id=activity_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    activity_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ActivityUpdate,
) -> ActivityResponse | HTTPValidationError | None:
    """Update Activity

    Args:
        activity_id (UUID):
        body (ActivityUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActivityResponse | HTTPValidationError
    """

    return sync_detailed(
        activity_id=activity_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    activity_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ActivityUpdate,
) -> Response[ActivityResponse | HTTPValidationError]:
    """Update Activity

    Args:
        activity_id (UUID):
        body (ActivityUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ActivityResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        activity_id=activity_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    activity_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ActivityUpdate,
) -> ActivityResponse | HTTPValidationError | None:
    """Update Activity

    Args:
        activity_id (UUID):
        body (ActivityUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ActivityResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            activity_id=activity_id,
            client=client,
            body=body,
        )
    ).parsed
