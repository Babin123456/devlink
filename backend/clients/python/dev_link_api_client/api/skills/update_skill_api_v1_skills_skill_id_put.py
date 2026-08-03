from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.skill_response import SkillResponse
from ...models.skill_update import SkillUpdate
from ...types import Response


def _get_kwargs(
    skill_id: UUID,
    *,
    body: SkillUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/skills/{skill_id}".format(
            skill_id=quote(str(skill_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SkillResponse | None:
    if response.status_code == 200:
        response_200 = SkillResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | SkillResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SkillUpdate,
) -> Response[HTTPValidationError | SkillResponse]:
    """Update Skill

    Args:
        skill_id (UUID):
        body (SkillUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SkillResponse]
    """

    kwargs = _get_kwargs(
        skill_id=skill_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SkillUpdate,
) -> HTTPValidationError | SkillResponse | None:
    """Update Skill

    Args:
        skill_id (UUID):
        body (SkillUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SkillResponse
    """

    return sync_detailed(
        skill_id=skill_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SkillUpdate,
) -> Response[HTTPValidationError | SkillResponse]:
    """Update Skill

    Args:
        skill_id (UUID):
        body (SkillUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SkillResponse]
    """

    kwargs = _get_kwargs(
        skill_id=skill_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: SkillUpdate,
) -> HTTPValidationError | SkillResponse | None:
    """Update Skill

    Args:
        skill_id (UUID):
        body (SkillUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SkillResponse
    """

    return (
        await asyncio_detailed(
            skill_id=skill_id,
            client=client,
            body=body,
        )
    ).parsed
