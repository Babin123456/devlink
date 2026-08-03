from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hackathon_team_create import HackathonTeamCreate
from ...models.hackathon_team_response import HackathonTeamResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    hackathon_id: UUID,
    *,
    body: HackathonTeamCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/hackathons/{hackathon_id}/teams".format(
            hackathon_id=quote(str(hackathon_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | HackathonTeamResponse | None:
    if response.status_code == 201:
        response_201 = HackathonTeamResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | HackathonTeamResponse]:
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
    body: HackathonTeamCreate,
) -> Response[HTTPValidationError | HackathonTeamResponse]:
    """Create Team

    Args:
        hackathon_id (UUID):
        body (HackathonTeamCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonTeamResponse]
    """

    kwargs = _get_kwargs(
        hackathon_id=hackathon_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonTeamCreate,
) -> HTTPValidationError | HackathonTeamResponse | None:
    """Create Team

    Args:
        hackathon_id (UUID):
        body (HackathonTeamCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonTeamResponse
    """

    return sync_detailed(
        hackathon_id=hackathon_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonTeamCreate,
) -> Response[HTTPValidationError | HackathonTeamResponse]:
    """Create Team

    Args:
        hackathon_id (UUID):
        body (HackathonTeamCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonTeamResponse]
    """

    kwargs = _get_kwargs(
        hackathon_id=hackathon_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonTeamCreate,
) -> HTTPValidationError | HackathonTeamResponse | None:
    """Create Team

    Args:
        hackathon_id (UUID):
        body (HackathonTeamCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonTeamResponse
    """

    return (
        await asyncio_detailed(
            hackathon_id=hackathon_id,
            client=client,
            body=body,
        )
    ).parsed
