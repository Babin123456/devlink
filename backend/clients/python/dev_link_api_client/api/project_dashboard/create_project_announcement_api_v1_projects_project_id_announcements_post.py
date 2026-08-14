from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.announcement_create import AnnouncementCreate
from ...models.announcement_response import AnnouncementResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    project_id: UUID,
    *,
    body: AnnouncementCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/projects/{project_id}/announcements".format(
            project_id=quote(str(project_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AnnouncementResponse | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = AnnouncementResponse.from_dict(response.json())

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
) -> Response[AnnouncementResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AnnouncementCreate,
) -> Response[AnnouncementResponse | HTTPValidationError]:
    """Post Announcement to Project

     Posts a team announcement on the project dashboard.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        body (AnnouncementCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnouncementResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AnnouncementCreate,
) -> AnnouncementResponse | HTTPValidationError | None:
    """Post Announcement to Project

     Posts a team announcement on the project dashboard.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        body (AnnouncementCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnouncementResponse | HTTPValidationError
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AnnouncementCreate,
) -> Response[AnnouncementResponse | HTTPValidationError]:
    """Post Announcement to Project

     Posts a team announcement on the project dashboard.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        body (AnnouncementCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnouncementResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: AnnouncementCreate,
) -> AnnouncementResponse | HTTPValidationError | None:
    """Post Announcement to Project

     Posts a team announcement on the project dashboard.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        body (AnnouncementCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnouncementResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
