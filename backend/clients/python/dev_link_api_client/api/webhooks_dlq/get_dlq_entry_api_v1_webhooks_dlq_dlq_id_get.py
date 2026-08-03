from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.webhook_dlq_response import WebhookDLQResponse
from ...types import Response


def _get_kwargs(
    dlq_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/webhooks/dlq/{dlq_id}".format(
            dlq_id=quote(str(dlq_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | WebhookDLQResponse | None:
    if response.status_code == 200:
        response_200 = WebhookDLQResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | WebhookDLQResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dlq_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | WebhookDLQResponse]:
    """Get DLQ entry details

     Get single DLQ entry.

    Args:
        dlq_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | WebhookDLQResponse]
    """

    kwargs = _get_kwargs(
        dlq_id=dlq_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dlq_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | WebhookDLQResponse | None:
    """Get DLQ entry details

     Get single DLQ entry.

    Args:
        dlq_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | WebhookDLQResponse
    """

    return sync_detailed(
        dlq_id=dlq_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    dlq_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | WebhookDLQResponse]:
    """Get DLQ entry details

     Get single DLQ entry.

    Args:
        dlq_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | WebhookDLQResponse]
    """

    kwargs = _get_kwargs(
        dlq_id=dlq_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dlq_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | WebhookDLQResponse | None:
    """Get DLQ entry details

     Get single DLQ entry.

    Args:
        dlq_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | WebhookDLQResponse
    """

    return (
        await asyncio_detailed(
            dlq_id=dlq_id,
            client=client,
        )
    ).parsed
