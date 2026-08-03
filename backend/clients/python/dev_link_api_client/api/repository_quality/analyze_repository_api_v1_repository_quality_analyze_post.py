from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.repository_quality_request import RepositoryQualityRequest
from ...models.repository_quality_response import RepositoryQualityResponse
from ...types import Response


def _get_kwargs(
    *,
    body: RepositoryQualityRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/repository-quality/analyze",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RepositoryQualityResponse | None:
    if response.status_code == 200:
        response_200 = RepositoryQualityResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | RepositoryQualityResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RepositoryQualityRequest,
) -> Response[HTTPValidationError | RepositoryQualityResponse]:
    """Analyze a GitHub repository's quality

     Analyze a GitHub repository and return an overall quality score
    with individual metric breakdown and improvement suggestions.

    **Metrics analyzed:**

    | Metric          | Weight | Description |
    | --------------- | ------ | ----------- |
    | README          | 0.20   | Quality and completeness of README |
    | Documentation   | 0.15   | Presence of docs/, guides, changelog |
    | License         | 0.10   | License file presence |
    | Test Coverage   | 0.20   | Test directories, test files, coverage config |
    | CI/CD           | 0.15   | GitHub Actions, CI config files |
    | Recent Activity | 0.10   | Commit recency and frequency |
    | Open Issues     | 0.10   | Issue backlog ratio |

    Results are cached for 30 minutes.

    Args:
        body (RepositoryQualityRequest): Request body for repository quality analysis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RepositoryQualityResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: RepositoryQualityRequest,
) -> HTTPValidationError | RepositoryQualityResponse | None:
    """Analyze a GitHub repository's quality

     Analyze a GitHub repository and return an overall quality score
    with individual metric breakdown and improvement suggestions.

    **Metrics analyzed:**

    | Metric          | Weight | Description |
    | --------------- | ------ | ----------- |
    | README          | 0.20   | Quality and completeness of README |
    | Documentation   | 0.15   | Presence of docs/, guides, changelog |
    | License         | 0.10   | License file presence |
    | Test Coverage   | 0.20   | Test directories, test files, coverage config |
    | CI/CD           | 0.15   | GitHub Actions, CI config files |
    | Recent Activity | 0.10   | Commit recency and frequency |
    | Open Issues     | 0.10   | Issue backlog ratio |

    Results are cached for 30 minutes.

    Args:
        body (RepositoryQualityRequest): Request body for repository quality analysis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RepositoryQualityResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RepositoryQualityRequest,
) -> Response[HTTPValidationError | RepositoryQualityResponse]:
    """Analyze a GitHub repository's quality

     Analyze a GitHub repository and return an overall quality score
    with individual metric breakdown and improvement suggestions.

    **Metrics analyzed:**

    | Metric          | Weight | Description |
    | --------------- | ------ | ----------- |
    | README          | 0.20   | Quality and completeness of README |
    | Documentation   | 0.15   | Presence of docs/, guides, changelog |
    | License         | 0.10   | License file presence |
    | Test Coverage   | 0.20   | Test directories, test files, coverage config |
    | CI/CD           | 0.15   | GitHub Actions, CI config files |
    | Recent Activity | 0.10   | Commit recency and frequency |
    | Open Issues     | 0.10   | Issue backlog ratio |

    Results are cached for 30 minutes.

    Args:
        body (RepositoryQualityRequest): Request body for repository quality analysis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RepositoryQualityResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RepositoryQualityRequest,
) -> HTTPValidationError | RepositoryQualityResponse | None:
    """Analyze a GitHub repository's quality

     Analyze a GitHub repository and return an overall quality score
    with individual metric breakdown and improvement suggestions.

    **Metrics analyzed:**

    | Metric          | Weight | Description |
    | --------------- | ------ | ----------- |
    | README          | 0.20   | Quality and completeness of README |
    | Documentation   | 0.15   | Presence of docs/, guides, changelog |
    | License         | 0.10   | License file presence |
    | Test Coverage   | 0.20   | Test directories, test files, coverage config |
    | CI/CD           | 0.15   | GitHub Actions, CI config files |
    | Recent Activity | 0.10   | Commit recency and frequency |
    | Open Issues     | 0.10   | Issue backlog ratio |

    Results are cached for 30 minutes.

    Args:
        body (RepositoryQualityRequest): Request body for repository quality analysis.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RepositoryQualityResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
