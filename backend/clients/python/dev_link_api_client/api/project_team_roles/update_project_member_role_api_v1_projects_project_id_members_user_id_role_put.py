from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_member_response import ProjectMemberResponse
from ...models.update_project_member_role_request import UpdateProjectMemberRoleRequest
from ...types import Response


def _get_kwargs(
    project_id: UUID,
    user_id: UUID,
    *,
    body: UpdateProjectMemberRoleRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/projects/{project_id}/members/{user_id}/role".format(
            project_id=quote(str(project_id), safe=""),
            user_id=quote(str(user_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProjectMemberResponse | None:
    if response.status_code == 200:
        response_200 = ProjectMemberResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProjectMemberResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMemberRoleRequest,
) -> Response[HTTPValidationError | ProjectMemberResponse]:
    """Assign or change a project member's role

     Assign or update team member role (Owner, Maintainer, Contributor, Reviewer, Viewer).

    Args:
        project_id (UUID):
        user_id (UUID):
        body (UpdateProjectMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectMemberResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMemberRoleRequest,
) -> HTTPValidationError | ProjectMemberResponse | None:
    """Assign or change a project member's role

     Assign or update team member role (Owner, Maintainer, Contributor, Reviewer, Viewer).

    Args:
        project_id (UUID):
        user_id (UUID):
        body (UpdateProjectMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectMemberResponse
    """

    return sync_detailed(
        project_id=project_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMemberRoleRequest,
) -> Response[HTTPValidationError | ProjectMemberResponse]:
    """Assign or change a project member's role

     Assign or update team member role (Owner, Maintainer, Contributor, Reviewer, Viewer).

    Args:
        project_id (UUID):
        user_id (UUID):
        body (UpdateProjectMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectMemberResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateProjectMemberRoleRequest,
) -> HTTPValidationError | ProjectMemberResponse | None:
    """Assign or change a project member's role

     Assign or update team member role (Owner, Maintainer, Contributor, Reviewer, Viewer).

    Args:
        project_id (UUID):
        user_id (UUID):
        body (UpdateProjectMemberRoleRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectMemberResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
