from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.revoke_session_response import RevokeSessionResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    current_session_id: None | Unset | UUID = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_current_session_id: None | str | Unset
    if isinstance(current_session_id, Unset):
        json_current_session_id = UNSET
    elif isinstance(current_session_id, UUID):
        json_current_session_id = str(current_session_id)
    else:
        json_current_session_id = current_session_id
    params["current_session_id"] = json_current_session_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/sessions/revoke-others",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RevokeSessionResponse | None:
    if response.status_code == 200:
        response_200 = RevokeSessionResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | RevokeSessionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    current_session_id: None | Unset | UUID = UNSET,
) -> Response[HTTPValidationError | RevokeSessionResponse]:
    """Revoke All Other Sessions

     Revoke all active sessions for current user except the current session.

    Args:
        current_session_id (None | Unset | UUID): Current session ID to keep active

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RevokeSessionResponse]
    """

    kwargs = _get_kwargs(
        current_session_id=current_session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    current_session_id: None | Unset | UUID = UNSET,
) -> HTTPValidationError | RevokeSessionResponse | None:
    """Revoke All Other Sessions

     Revoke all active sessions for current user except the current session.

    Args:
        current_session_id (None | Unset | UUID): Current session ID to keep active

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RevokeSessionResponse
    """

    return sync_detailed(
        client=client,
        current_session_id=current_session_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    current_session_id: None | Unset | UUID = UNSET,
) -> Response[HTTPValidationError | RevokeSessionResponse]:
    """Revoke All Other Sessions

     Revoke all active sessions for current user except the current session.

    Args:
        current_session_id (None | Unset | UUID): Current session ID to keep active

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RevokeSessionResponse]
    """

    kwargs = _get_kwargs(
        current_session_id=current_session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    current_session_id: None | Unset | UUID = UNSET,
) -> HTTPValidationError | RevokeSessionResponse | None:
    """Revoke All Other Sessions

     Revoke all active sessions for current user except the current session.

    Args:
        current_session_id (None | Unset | UUID): Current session ID to keep active

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RevokeSessionResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            current_session_id=current_session_id,
        )
    ).parsed
