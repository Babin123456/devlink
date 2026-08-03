from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.milestone_response import MilestoneResponse
from ...types import UNSET, Response


def _get_kwargs(
    project_id: UUID,
    milestone_id: UUID,
    *,
    is_completed: bool,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["is_completed"] = is_completed

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/projects/{project_id}/milestones/{milestone_id}/complete".format(
            project_id=quote(str(project_id), safe=""),
            milestone_id=quote(str(milestone_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | MilestoneResponse | None:
    if response.status_code == 200:
        response_200 = MilestoneResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | MilestoneResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient,
    is_completed: bool,
) -> Response[HTTPValidationError | MilestoneResponse]:
    """Mark Milestone as Completed or Reopened

     Marks a milestone as completed or reopens it.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        milestone_id (UUID):
        is_completed (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MilestoneResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        milestone_id=milestone_id,
        is_completed=is_completed,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient,
    is_completed: bool,
) -> HTTPValidationError | MilestoneResponse | None:
    """Mark Milestone as Completed or Reopened

     Marks a milestone as completed or reopens it.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        milestone_id (UUID):
        is_completed (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MilestoneResponse
    """

    return sync_detailed(
        project_id=project_id,
        milestone_id=milestone_id,
        client=client,
        is_completed=is_completed,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient,
    is_completed: bool,
) -> Response[HTTPValidationError | MilestoneResponse]:
    """Mark Milestone as Completed or Reopened

     Marks a milestone as completed or reopens it.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        milestone_id (UUID):
        is_completed (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MilestoneResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        milestone_id=milestone_id,
        is_completed=is_completed,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    milestone_id: UUID,
    *,
    client: AuthenticatedClient,
    is_completed: bool,
) -> HTTPValidationError | MilestoneResponse | None:
    """Mark Milestone as Completed or Reopened

     Marks a milestone as completed or reopens it.
    Restricted to Owners, Co-Owners, Admins, and Maintainers.

    Args:
        project_id (UUID):
        milestone_id (UUID):
        is_completed (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MilestoneResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            milestone_id=milestone_id,
            client=client,
            is_completed=is_completed,
        )
    ).parsed
