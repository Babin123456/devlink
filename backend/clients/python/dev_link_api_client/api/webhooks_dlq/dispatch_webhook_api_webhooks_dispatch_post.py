from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.webhook_delivery_response import WebhookDeliveryResponse
from ...models.webhook_dispatch_params import WebhookDispatchParams
from ...types import Response


def _get_kwargs(
    *,
    body: WebhookDispatchParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/webhooks/dispatch",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | WebhookDeliveryResponse | None:
    if response.status_code == 201:
        response_201 = WebhookDeliveryResponse.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | WebhookDeliveryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: WebhookDispatchParams,
) -> Response[HTTPValidationError | WebhookDeliveryResponse]:
    """Dispatch a new webhook event with automatic retry

     Dispatch a webhook to a target URL with automatic retries and dead letter queue fallback.

    Args:
        body (WebhookDispatchParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | WebhookDeliveryResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: WebhookDispatchParams,
) -> HTTPValidationError | WebhookDeliveryResponse | None:
    """Dispatch a new webhook event with automatic retry

     Dispatch a webhook to a target URL with automatic retries and dead letter queue fallback.

    Args:
        body (WebhookDispatchParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | WebhookDeliveryResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: WebhookDispatchParams,
) -> Response[HTTPValidationError | WebhookDeliveryResponse]:
    """Dispatch a new webhook event with automatic retry

     Dispatch a webhook to a target URL with automatic retries and dead letter queue fallback.

    Args:
        body (WebhookDispatchParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | WebhookDeliveryResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: WebhookDispatchParams,
) -> HTTPValidationError | WebhookDeliveryResponse | None:
    """Dispatch a new webhook event with automatic retry

     Dispatch a webhook to a target URL with automatic retries and dead letter queue fallback.

    Args:
        body (WebhookDispatchParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | WebhookDeliveryResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
