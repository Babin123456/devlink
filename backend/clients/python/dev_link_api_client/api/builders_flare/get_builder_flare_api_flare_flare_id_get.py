from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.builder_flare_response import BuilderFlareResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    flare_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/flare/{flare_id}".format(
            flare_id=quote(str(flare_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BuilderFlareResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = BuilderFlareResponse.from_dict(response.json())

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
) -> Response[BuilderFlareResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    flare_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BuilderFlareResponse | HTTPValidationError]:
    """Get Builder Flare

    Args:
        flare_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuilderFlareResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        flare_id=flare_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    flare_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> BuilderFlareResponse | HTTPValidationError | None:
    """Get Builder Flare

    Args:
        flare_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuilderFlareResponse | HTTPValidationError
    """

    return sync_detailed(
        flare_id=flare_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    flare_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BuilderFlareResponse | HTTPValidationError]:
    """Get Builder Flare

    Args:
        flare_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BuilderFlareResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        flare_id=flare_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    flare_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> BuilderFlareResponse | HTTPValidationError | None:
    """Get Builder Flare

    Args:
        flare_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BuilderFlareResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            flare_id=flare_id,
            client=client,
        )
    ).parsed
