from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.search_indexed_response import SearchIndexedResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str | Unset = "",
    category: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    json_category: None | str | Unset
    if isinstance(category, Unset):
        json_category = UNSET
    else:
        json_category = category
    params["category"] = json_category

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/search/indexed",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SearchIndexedResponse | None:
    if response.status_code == 200:
        response_200 = SearchIndexedResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | SearchIndexedResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "",
    category: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | SearchIndexedResponse]:
    """Optimized global index search

     Executes high-performance tokenized search across inverted index with weighted relevance ranking.

    Args:
        q (str | Unset): Search query string Default: ''.
        category (None | str | Unset): Resource category: developers, projects, organizations,
            discussions, skills, technologies
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SearchIndexedResponse]
    """

    kwargs = _get_kwargs(
        q=q,
        category=category,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "",
    category: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
) -> HTTPValidationError | SearchIndexedResponse | None:
    """Optimized global index search

     Executes high-performance tokenized search across inverted index with weighted relevance ranking.

    Args:
        q (str | Unset): Search query string Default: ''.
        category (None | str | Unset): Resource category: developers, projects, organizations,
            discussions, skills, technologies
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SearchIndexedResponse
    """

    return sync_detailed(
        client=client,
        q=q,
        category=category,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "",
    category: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | SearchIndexedResponse]:
    """Optimized global index search

     Executes high-performance tokenized search across inverted index with weighted relevance ranking.

    Args:
        q (str | Unset): Search query string Default: ''.
        category (None | str | Unset): Resource category: developers, projects, organizations,
            discussions, skills, technologies
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SearchIndexedResponse]
    """

    kwargs = _get_kwargs(
        q=q,
        category=category,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "",
    category: None | str | Unset = UNSET,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
) -> HTTPValidationError | SearchIndexedResponse | None:
    """Optimized global index search

     Executes high-performance tokenized search across inverted index with weighted relevance ranking.

    Args:
        q (str | Unset): Search query string Default: ''.
        category (None | str | Unset): Resource category: developers, projects, organizations,
            discussions, skills, technologies
        limit (int | Unset):  Default: 20.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SearchIndexedResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            category=category,
            limit=limit,
            offset=offset,
        )
    ).parsed
