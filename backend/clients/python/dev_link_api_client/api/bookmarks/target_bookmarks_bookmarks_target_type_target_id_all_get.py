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
        "method": "get",
        "url": "/bookmarks/{target_type}/{target_id}/all".format(
            target_type=quote(str(target_type), safe=""),
            target_id=quote(str(target_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[BookmarkResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BookmarkResponse.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[BookmarkResponse]]:
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
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[BookmarkResponse]]:
    """Target Bookmarks

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[BookmarkResponse]]
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
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[BookmarkResponse] | None:
    """Target Bookmarks

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[BookmarkResponse]
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
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[BookmarkResponse]]:
    """Target Bookmarks

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[BookmarkResponse]]
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
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[BookmarkResponse] | None:
    """Target Bookmarks

    Args:
        target_type (BookmarkTargetType):
        target_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[BookmarkResponse]
    """

    return (
        await asyncio_detailed(
            target_type=target_type,
            target_id=target_id,
            client=client,
        )
    ).parsed
