from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.activity_response import ActivityResponse
from ...models.activity_type import ActivityType
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    activity_type: ActivityType,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/activities/type/{activity_type}".format(
            activity_type=quote(str(activity_type), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ActivityResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ActivityResponse.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[ActivityResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    activity_type: ActivityType,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[ActivityResponse]]:
    """Activities By Type

    Args:
        activity_type (ActivityType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ActivityResponse]]
    """

    kwargs = _get_kwargs(
        activity_type=activity_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    activity_type: ActivityType,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[ActivityResponse] | None:
    """Activities By Type

    Args:
        activity_type (ActivityType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ActivityResponse]
    """

    return sync_detailed(
        activity_type=activity_type,
        client=client,
    ).parsed


async def asyncio_detailed(
    activity_type: ActivityType,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[ActivityResponse]]:
    """Activities By Type

    Args:
        activity_type (ActivityType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ActivityResponse]]
    """

    kwargs = _get_kwargs(
        activity_type=activity_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    activity_type: ActivityType,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[ActivityResponse] | None:
    """Activities By Type

    Args:
        activity_type (ActivityType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ActivityResponse]
    """

    return (
        await asyncio_detailed(
            activity_type=activity_type,
            client=client,
        )
    ).parsed
