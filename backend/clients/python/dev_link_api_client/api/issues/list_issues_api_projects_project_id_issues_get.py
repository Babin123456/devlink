from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.issue_response import IssueResponse
from ...models.issue_status import IssueStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: UUID,
    *,
    status: IssueStatus | None | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, IssueStatus):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/projects/{project_id}/issues".format(
            project_id=quote(str(project_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[IssueResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = IssueResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[IssueResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    status: IssueStatus | None | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | list[IssueResponse]]:
    """List Issues

     List all issues in a project.

    Args:
        project_id (UUID):
        status (IssueStatus | None | Unset):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[IssueResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        status=status,
        skip=skip,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    status: IssueStatus | None | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
) -> HTTPValidationError | list[IssueResponse] | None:
    """List Issues

     List all issues in a project.

    Args:
        project_id (UUID):
        status (IssueStatus | None | Unset):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[IssueResponse]
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        status=status,
        skip=skip,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    status: IssueStatus | None | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | list[IssueResponse]]:
    """List Issues

     List all issues in a project.

    Args:
        project_id (UUID):
        status (IssueStatus | None | Unset):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[IssueResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        status=status,
        skip=skip,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    status: IssueStatus | None | Unset = UNSET,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
) -> HTTPValidationError | list[IssueResponse] | None:
    """List Issues

     List all issues in a project.

    Args:
        project_id (UUID):
        status (IssueStatus | None | Unset):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[IssueResponse]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            status=status,
            skip=skip,
            limit=limit,
        )
    ).parsed
