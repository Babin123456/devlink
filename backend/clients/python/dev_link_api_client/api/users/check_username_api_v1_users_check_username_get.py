from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.username_availability_response import UsernameAvailabilityResponse
from ...types import UNSET, Response


def _get_kwargs(
    *,
    username: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/users/check-username",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UsernameAvailabilityResponse | None:
    if response.status_code == 200:
        response_200 = UsernameAvailabilityResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | UsernameAvailabilityResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    username: str,
) -> Response[HTTPValidationError | UsernameAvailabilityResponse]:
    """Check Username Availability

     Check if a username is available for registration.

    Args:
        username (str): The username to check availability for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsernameAvailabilityResponse]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    username: str,
) -> HTTPValidationError | UsernameAvailabilityResponse | None:
    """Check Username Availability

     Check if a username is available for registration.

    Args:
        username (str): The username to check availability for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsernameAvailabilityResponse
    """

    return sync_detailed(
        client=client,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    username: str,
) -> Response[HTTPValidationError | UsernameAvailabilityResponse]:
    """Check Username Availability

     Check if a username is available for registration.

    Args:
        username (str): The username to check availability for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UsernameAvailabilityResponse]
    """

    kwargs = _get_kwargs(
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    username: str,
) -> HTTPValidationError | UsernameAvailabilityResponse | None:
    """Check Username Availability

     Check if a username is available for registration.

    Args:
        username (str): The username to check availability for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UsernameAvailabilityResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            username=username,
        )
    ).parsed
