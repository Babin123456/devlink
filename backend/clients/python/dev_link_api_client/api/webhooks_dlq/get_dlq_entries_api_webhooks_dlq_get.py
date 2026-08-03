from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.webhook_dlq_paginated_response import WebhookDLQPaginatedResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    is_replayed: bool | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    json_is_replayed: bool | None | Unset
    if isinstance(is_replayed, Unset):
        json_is_replayed = UNSET
    else:
        json_is_replayed = is_replayed
    params["is_replayed"] = json_is_replayed

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/webhooks/dlq",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | WebhookDLQPaginatedResponse | None:
    if response.status_code == 200:
        response_200 = WebhookDLQPaginatedResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | WebhookDLQPaginatedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    is_replayed: bool | None | Unset = UNSET,
) -> Response[HTTPValidationError | WebhookDLQPaginatedResponse]:
    """List Dead Letter Queue (DLQ) entries

     Retrieve paginated entries from the Webhook Dead Letter Queue.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        is_replayed (bool | None | Unset): Filter by replayed status

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | WebhookDLQPaginatedResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        is_replayed=is_replayed,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    is_replayed: bool | None | Unset = UNSET,
) -> HTTPValidationError | WebhookDLQPaginatedResponse | None:
    """List Dead Letter Queue (DLQ) entries

     Retrieve paginated entries from the Webhook Dead Letter Queue.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        is_replayed (bool | None | Unset): Filter by replayed status

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | WebhookDLQPaginatedResponse
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        is_replayed=is_replayed,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    is_replayed: bool | None | Unset = UNSET,
) -> Response[HTTPValidationError | WebhookDLQPaginatedResponse]:
    """List Dead Letter Queue (DLQ) entries

     Retrieve paginated entries from the Webhook Dead Letter Queue.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        is_replayed (bool | None | Unset): Filter by replayed status

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | WebhookDLQPaginatedResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        is_replayed=is_replayed,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    is_replayed: bool | None | Unset = UNSET,
) -> HTTPValidationError | WebhookDLQPaginatedResponse | None:
    """List Dead Letter Queue (DLQ) entries

     Retrieve paginated entries from the Webhook Dead Letter Queue.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        is_replayed (bool | None | Unset): Filter by replayed status

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | WebhookDLQPaginatedResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            is_replayed=is_replayed,
        )
    ).parsed
