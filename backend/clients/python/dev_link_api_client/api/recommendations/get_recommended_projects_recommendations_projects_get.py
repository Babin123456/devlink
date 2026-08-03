from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_recommendation_response import ProjectRecommendationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: int | Unset = 20,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/recommendations/projects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProjectRecommendationResponse | None:
    if response.status_code == 200:
        response_200 = ProjectRecommendationResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProjectRecommendationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | ProjectRecommendationResponse]:
    """Get recommended projects

     Returns a ranked list of recommended projects for the authenticated developer.

    **Scoring factors**:
    - **Skills**: Project requirements vs Developer's skills
    - **Technologies**: Project tech stack vs Developer's skills
    - **Experience**: Project minimum experience vs Developer's experience
    - **Interests**: Project title/description vs Developer's bio/headline

    Args:
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectRecommendationResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> HTTPValidationError | ProjectRecommendationResponse | None:
    """Get recommended projects

     Returns a ranked list of recommended projects for the authenticated developer.

    **Scoring factors**:
    - **Skills**: Project requirements vs Developer's skills
    - **Technologies**: Project tech stack vs Developer's skills
    - **Experience**: Project minimum experience vs Developer's experience
    - **Interests**: Project title/description vs Developer's bio/headline

    Args:
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectRecommendationResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | ProjectRecommendationResponse]:
    """Get recommended projects

     Returns a ranked list of recommended projects for the authenticated developer.

    **Scoring factors**:
    - **Skills**: Project requirements vs Developer's skills
    - **Technologies**: Project tech stack vs Developer's skills
    - **Experience**: Project minimum experience vs Developer's experience
    - **Interests**: Project title/description vs Developer's bio/headline

    Args:
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectRecommendationResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 20,
) -> HTTPValidationError | ProjectRecommendationResponse | None:
    """Get recommended projects

     Returns a ranked list of recommended projects for the authenticated developer.

    **Scoring factors**:
    - **Skills**: Project requirements vs Developer's skills
    - **Technologies**: Project tech stack vs Developer's skills
    - **Experience**: Project minimum experience vs Developer's experience
    - **Interests**: Project title/description vs Developer's bio/headline

    Args:
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectRecommendationResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
        )
    ).parsed
