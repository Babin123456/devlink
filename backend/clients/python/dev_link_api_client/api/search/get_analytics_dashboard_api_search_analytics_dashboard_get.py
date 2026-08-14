from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_analytics_dashboard_api_search_analytics_dashboard_get_response_get_analytics_dashboard_api_search_analytics_dashboard_get import (
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    days: int | Unset = 30,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["days"] = days

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/search/analytics/dashboard",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet
    | HTTPValidationError
    | None
):
    if response.status_code == 200:
        response_200 = GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet.from_dict(
            response.json()
        )

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
) -> Response[
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet
    | HTTPValidationError
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
) -> Response[
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet
    | HTTPValidationError
]:
    """Get search analytics dashboard metrics

    Args:
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        days=days,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
) -> (
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet
    | HTTPValidationError
    | None
):
    """Get search analytics dashboard metrics

    Args:
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        days=days,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
) -> Response[
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet
    | HTTPValidationError
]:
    """Get search analytics dashboard metrics

    Args:
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        days=days,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,
) -> (
    GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet
    | HTTPValidationError
    | None
):
    """Get search analytics dashboard metrics

    Args:
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAnalyticsDashboardApiSearchAnalyticsDashboardGetResponseGetAnalyticsDashboardApiSearchAnalyticsDashboardGet | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            days=days,
        )
    ).parsed
