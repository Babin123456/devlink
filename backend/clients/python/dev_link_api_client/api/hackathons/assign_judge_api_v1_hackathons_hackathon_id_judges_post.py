from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hackathon_judge_response import HackathonJudgeResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    hackathon_id: UUID,
    *,
    user_id: UUID,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_user_id = str(user_id)
    params["user_id"] = json_user_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/hackathons/{hackathon_id}/judges".format(
            hackathon_id=quote(str(hackathon_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | HackathonJudgeResponse | None:
    if response.status_code == 201:
        response_201 = HackathonJudgeResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | HackathonJudgeResponse]:
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
    user_id: UUID,
) -> Response[HTTPValidationError | HackathonJudgeResponse]:
    """Assign Judge

    Args:
        hackathon_id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonJudgeResponse]
    """

    kwargs = _get_kwargs(
        hackathon_id=hackathon_id,
        user_id=user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
    user_id: UUID,
) -> HTTPValidationError | HackathonJudgeResponse | None:
    """Assign Judge

    Args:
        hackathon_id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonJudgeResponse
    """

    return sync_detailed(
        hackathon_id=hackathon_id,
        client=client,
        user_id=user_id,
    ).parsed


async def asyncio_detailed(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
    user_id: UUID,
) -> Response[HTTPValidationError | HackathonJudgeResponse]:
    """Assign Judge

    Args:
        hackathon_id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonJudgeResponse]
    """

    kwargs = _get_kwargs(
        hackathon_id=hackathon_id,
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hackathon_id: UUID,
    *,
    client: AuthenticatedClient,
    user_id: UUID,
) -> HTTPValidationError | HackathonJudgeResponse | None:
    """Assign Judge

    Args:
        hackathon_id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonJudgeResponse
    """

    return (
        await asyncio_detailed(
            hackathon_id=hackathon_id,
            client=client,
            user_id=user_id,
        )
    ).parsed
