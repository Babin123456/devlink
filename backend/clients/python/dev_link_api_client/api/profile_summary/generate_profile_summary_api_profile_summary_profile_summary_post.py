from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.profile_summary_request import ProfileSummaryRequest
from ...models.profile_summary_response import ProfileSummaryResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ProfileSummaryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/profile-summary/profile-summary",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProfileSummaryResponse | None:
    if response.status_code == 200:
        response_200 = ProfileSummaryResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProfileSummaryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ProfileSummaryRequest,
) -> Response[HTTPValidationError | ProfileSummaryResponse]:
    """Generate Profile Summary

     Generate an AI-powered professional summary for a developer profile.

    Creates a concise summary based on the user's profile data,
    skills, and activity. Limited to 500 characters.

    Args:
        body (ProfileSummaryRequest): Request to generate a profile summary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProfileSummaryResponse]
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
    body: ProfileSummaryRequest,
) -> HTTPValidationError | ProfileSummaryResponse | None:
    """Generate Profile Summary

     Generate an AI-powered professional summary for a developer profile.

    Creates a concise summary based on the user's profile data,
    skills, and activity. Limited to 500 characters.

    Args:
        body (ProfileSummaryRequest): Request to generate a profile summary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProfileSummaryResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProfileSummaryRequest,
) -> Response[HTTPValidationError | ProfileSummaryResponse]:
    """Generate Profile Summary

     Generate an AI-powered professional summary for a developer profile.

    Creates a concise summary based on the user's profile data,
    skills, and activity. Limited to 500 characters.

    Args:
        body (ProfileSummaryRequest): Request to generate a profile summary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProfileSummaryResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProfileSummaryRequest,
) -> HTTPValidationError | ProfileSummaryResponse | None:
    """Generate Profile Summary

     Generate an AI-powered professional summary for a developer profile.

    Creates a concise summary based on the user's profile data,
    skills, and activity. Limited to 500 characters.

    Args:
        body (ProfileSummaryRequest): Request to generate a profile summary.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProfileSummaryResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
