from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_analytics_response import ProjectAnalyticsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: UUID,
    *,
    days: int | Unset = 30,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["days"] = days

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/projects/{project_id}/analytics".format(
            project_id=quote(str(project_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProjectAnalyticsResponse | None:
    if response.status_code == 200:
        response_200 = ProjectAnalyticsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProjectAnalyticsResponse]:
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
    days: int | Unset = 30,
) -> Response[HTTPValidationError | ProjectAnalyticsResponse]:
    """Get Project View Analytics

     Get project view analytics including total views, unique viewers, and daily views.

    Args:
        project_id (UUID):
        days (int | Unset): Number of days for daily views breakdown Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectAnalyticsResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        days=days,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    days: int | Unset = 30,
) -> HTTPValidationError | ProjectAnalyticsResponse | None:
    """Get Project View Analytics

     Get project view analytics including total views, unique viewers, and daily views.

    Args:
        project_id (UUID):
        days (int | Unset): Number of days for daily views breakdown Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectAnalyticsResponse
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        days=days,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    days: int | Unset = 30,
) -> Response[HTTPValidationError | ProjectAnalyticsResponse]:
    """Get Project View Analytics

     Get project view analytics including total views, unique viewers, and daily views.

    Args:
        project_id (UUID):
        days (int | Unset): Number of days for daily views breakdown Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectAnalyticsResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        days=days,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    days: int | Unset = 30,
) -> HTTPValidationError | ProjectAnalyticsResponse | None:
    """Get Project View Analytics

     Get project view analytics including total views, unique viewers, and daily views.

    Args:
        project_id (UUID):
        days (int | Unset): Number of days for daily views breakdown Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectAnalyticsResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            days=days,
        )
    ).parsed
