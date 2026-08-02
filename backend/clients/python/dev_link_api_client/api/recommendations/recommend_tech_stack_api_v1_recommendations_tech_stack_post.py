from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.tech_stack_request import TechStackRequest
from ...models.tech_stack_response import TechStackResponse
from ...types import Response


def _get_kwargs(
    *,
    body: TechStackRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/recommendations/tech-stack",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | TechStackResponse | None:
    if response.status_code == 200:
        response_200 = TechStackResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | TechStackResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: TechStackRequest,
) -> Response[HTTPValidationError | TechStackResponse]:
    """Get AI tech stack recommendation

     Recommend technologies for a new project based on the project idea.

    Uses OpenAI to generate ranked recommendations with explanations.
    Falls back to rule-based recommendations if the AI service is unavailable.

    Args:
        body (TechStackRequest): Request body for AI tech stack recommendation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TechStackResponse]
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
    client: AuthenticatedClient | Client,
    body: TechStackRequest,
) -> HTTPValidationError | TechStackResponse | None:
    """Get AI tech stack recommendation

     Recommend technologies for a new project based on the project idea.

    Uses OpenAI to generate ranked recommendations with explanations.
    Falls back to rule-based recommendations if the AI service is unavailable.

    Args:
        body (TechStackRequest): Request body for AI tech stack recommendation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TechStackResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: TechStackRequest,
) -> Response[HTTPValidationError | TechStackResponse]:
    """Get AI tech stack recommendation

     Recommend technologies for a new project based on the project idea.

    Uses OpenAI to generate ranked recommendations with explanations.
    Falls back to rule-based recommendations if the AI service is unavailable.

    Args:
        body (TechStackRequest): Request body for AI tech stack recommendation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | TechStackResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: TechStackRequest,
) -> HTTPValidationError | TechStackResponse | None:
    """Get AI tech stack recommendation

     Recommend technologies for a new project based on the project idea.

    Uses OpenAI to generate ranked recommendations with explanations.
    Falls back to rule-based recommendations if the AI service is unavailable.

    Args:
        body (TechStackRequest): Request body for AI tech stack recommendation.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | TechStackResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
