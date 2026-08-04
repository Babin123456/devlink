from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.search_benchmark_report import SearchBenchmarkReport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str | Unset = "dev",
    iterations: int | Unset = 10,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["iterations"] = iterations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/search/benchmark",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SearchBenchmarkReport | None:
    if response.status_code == 200:
        response_200 = SearchBenchmarkReport.from_dict(response.json())

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
) -> Response[HTTPValidationError | SearchBenchmarkReport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "dev",
    iterations: int | Unset = 10,
) -> Response[HTTPValidationError | SearchBenchmarkReport]:
    """Run search index performance benchmark

     Benchmarks query execution latency comparing Inverted Index search vs Naive SQL ILIKE search.

    Args:
        q (str | Unset): Query to benchmark Default: 'dev'.
        iterations (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SearchBenchmarkReport]
    """

    kwargs = _get_kwargs(
        q=q,
        iterations=iterations,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "dev",
    iterations: int | Unset = 10,
) -> HTTPValidationError | SearchBenchmarkReport | None:
    """Run search index performance benchmark

     Benchmarks query execution latency comparing Inverted Index search vs Naive SQL ILIKE search.

    Args:
        q (str | Unset): Query to benchmark Default: 'dev'.
        iterations (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SearchBenchmarkReport
    """

    return sync_detailed(
        client=client,
        q=q,
        iterations=iterations,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "dev",
    iterations: int | Unset = 10,
) -> Response[HTTPValidationError | SearchBenchmarkReport]:
    """Run search index performance benchmark

     Benchmarks query execution latency comparing Inverted Index search vs Naive SQL ILIKE search.

    Args:
        q (str | Unset): Query to benchmark Default: 'dev'.
        iterations (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SearchBenchmarkReport]
    """

    kwargs = _get_kwargs(
        q=q,
        iterations=iterations,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    q: str | Unset = "dev",
    iterations: int | Unset = 10,
) -> HTTPValidationError | SearchBenchmarkReport | None:
    """Run search index performance benchmark

     Benchmarks query execution latency comparing Inverted Index search vs Naive SQL ILIKE search.

    Args:
        q (str | Unset): Query to benchmark Default: 'dev'.
        iterations (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SearchBenchmarkReport
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            iterations=iterations,
        )
    ).parsed
