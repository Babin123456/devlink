from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.current_user import CurrentUser
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    online_threshold: int | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_online_threshold: int | None | Unset
    if isinstance(online_threshold, Unset):
        json_online_threshold = UNSET
    else:
        json_online_threshold = online_threshold
    params["online_threshold"] = json_online_threshold

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/users/me",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CurrentUser | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CurrentUser.from_dict(response.json())

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
) -> Response[CurrentUser | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    online_threshold: int | None | Unset = UNSET,
) -> Response[CurrentUser | HTTPValidationError]:
    """Get Me

    Args:
        online_threshold (int | None | Unset): Online threshold in seconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CurrentUser | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        online_threshold=online_threshold,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    online_threshold: int | None | Unset = UNSET,
) -> CurrentUser | HTTPValidationError | None:
    """Get Me

    Args:
        online_threshold (int | None | Unset): Online threshold in seconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CurrentUser | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        online_threshold=online_threshold,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    online_threshold: int | None | Unset = UNSET,
) -> Response[CurrentUser | HTTPValidationError]:
    """Get Me

    Args:
        online_threshold (int | None | Unset): Online threshold in seconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CurrentUser | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        online_threshold=online_threshold,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    online_threshold: int | None | Unset = UNSET,
) -> CurrentUser | HTTPValidationError | None:
    """Get Me

    Args:
        online_threshold (int | None | Unset): Online threshold in seconds

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CurrentUser | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            online_threshold=online_threshold,
        )
    ).parsed
