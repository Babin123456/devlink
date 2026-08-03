from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hackathon_registration_response import HackathonRegistrationResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    hackathon_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/hackathons/{hackathon_id}/registrations".format(
            hackathon_id=quote(str(hackathon_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | HackathonRegistrationResponse | None:
    if response.status_code == 200:
        response_200 = HackathonRegistrationResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | HackathonRegistrationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | HackathonRegistrationResponse]:
    """Cancel Registration

    Args:
        hackathon_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonRegistrationResponse]
    """

    kwargs = _get_kwargs(
        hackathon_id=hackathon_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | HackathonRegistrationResponse | None:
    """Cancel Registration

    Args:
        hackathon_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonRegistrationResponse
    """

    return sync_detailed(
        hackathon_id=hackathon_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError | HackathonRegistrationResponse]:
    """Cancel Registration

    Args:
        hackathon_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonRegistrationResponse]
    """

    kwargs = _get_kwargs(
        hackathon_id=hackathon_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
) -> HTTPValidationError | HackathonRegistrationResponse | None:
    """Cancel Registration

    Args:
        hackathon_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonRegistrationResponse
    """

    return (
        await asyncio_detailed(
            hackathon_id=hackathon_id,
            client=client,
        )
    ).parsed
