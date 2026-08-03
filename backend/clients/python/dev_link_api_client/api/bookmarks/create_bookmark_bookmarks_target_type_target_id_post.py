from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bookmark_response import BookmarkResponse
from ...models.bookmark_target_type import BookmarkTargetType
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    target_type: BookmarkTargetType,
    target_id: UUID,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/bookmarks/{target_type}/{target_id}".format(
            target_type=quote(str(target_type), safe=""),
            target_id=quote(str(target_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BookmarkResponse | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = BookmarkResponse.from_dict(response.json())

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
) -> Response[BookmarkResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    target_type: BookmarkTargetType,
    target_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[BookmarkResponse | HTTPValidationError]:
    """Create Bookmark

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BookmarkResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        target_type=target_type,
        target_id=target_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    target_type: BookmarkTargetType,
    target_id: UUID,
    *,
    client: AuthenticatedClient,
) -> BookmarkResponse | HTTPValidationError | None:
    """Create Bookmark

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BookmarkResponse | HTTPValidationError
    """

    return sync_detailed(
        target_type=target_type,
        target_id=target_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    target_type: BookmarkTargetType,
    target_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[BookmarkResponse | HTTPValidationError]:
    """Create Bookmark

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BookmarkResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        target_type=target_type,
        target_id=target_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    target_type: BookmarkTargetType,
    target_id: UUID,
    *,
    client: AuthenticatedClient,
) -> BookmarkResponse | HTTPValidationError | None:
    """Create Bookmark

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BookmarkResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            target_type=target_type,
            target_id=target_id,
            client=client,
        )
    ).parsed
