from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.recommendation_response import RecommendationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_id: None | Unset | UUID = UNSET,
    limit: int | Unset = 20,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_project_id: None | str | Unset
    if isinstance(project_id, Unset):
        json_project_id = UNSET
    elif isinstance(project_id, UUID):
        json_project_id = str(project_id)
    else:
        json_project_id = project_id
    params["project_id"] = json_project_id

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/recommendations/builders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecommendationResponse | None:
    if response.status_code == 200:
        response_200 = RecommendationResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | RecommendationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: None | Unset | UUID = UNSET,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | RecommendationResponse]:
    """Get recommended builders (collaborators)

     Returns a ranked list of recommended builders (potential collaborators).

    **Scoring factors** (each in ``[0, 1]``):

    | Factor          | Weight | Source |
    | --------------- | ------ | ------ |
    | Skills          | 0.30   | Jaccard overlap weighted by skill level |
    | Technologies   | 0.20   | Builder skills vs. ``project.tech_stack`` |
    | Experience      | 0.15   | Builder years vs. ``project_skill.minimum_experience`` |
    | Interests       | 0.10   | Bio/headline keyword overlap with project description |
    | Availability    | 0.10   | ``user.open_to_work`` |
    | Contributions   | 0.10   | Owned projects + accepted applications (log scale) |
    | Network         | 0.05   | Mutual-follower social boost |

    Results are cached for 10 minutes.

    Args:
        project_id (None | Unset | UUID): Optional project ID. When supplied, builders are ranked
            against that project's required skills, tech stack and minimum experience. When omitted,
            builders are ranked against the requester's own profile (find-collaborators mode).
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecommendationResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id: None | Unset | UUID = UNSET,
    limit: int | Unset = 20,
) -> HTTPValidationError | RecommendationResponse | None:
    """Get recommended builders (collaborators)

     Returns a ranked list of recommended builders (potential collaborators).

    **Scoring factors** (each in ``[0, 1]``):

    | Factor          | Weight | Source |
    | --------------- | ------ | ------ |
    | Skills          | 0.30   | Jaccard overlap weighted by skill level |
    | Technologies   | 0.20   | Builder skills vs. ``project.tech_stack`` |
    | Experience      | 0.15   | Builder years vs. ``project_skill.minimum_experience`` |
    | Interests       | 0.10   | Bio/headline keyword overlap with project description |
    | Availability    | 0.10   | ``user.open_to_work`` |
    | Contributions   | 0.10   | Owned projects + accepted applications (log scale) |
    | Network         | 0.05   | Mutual-follower social boost |

    Results are cached for 10 minutes.

    Args:
        project_id (None | Unset | UUID): Optional project ID. When supplied, builders are ranked
            against that project's required skills, tech stack and minimum experience. When omitted,
            builders are ranked against the requester's own profile (find-collaborators mode).
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecommendationResponse
    """

    return sync_detailed(
        client=client,
        project_id=project_id,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: None | Unset | UUID = UNSET,
    limit: int | Unset = 20,
) -> Response[HTTPValidationError | RecommendationResponse]:
    """Get recommended builders (collaborators)

     Returns a ranked list of recommended builders (potential collaborators).

    **Scoring factors** (each in ``[0, 1]``):

    | Factor          | Weight | Source |
    | --------------- | ------ | ------ |
    | Skills          | 0.30   | Jaccard overlap weighted by skill level |
    | Technologies   | 0.20   | Builder skills vs. ``project.tech_stack`` |
    | Experience      | 0.15   | Builder years vs. ``project_skill.minimum_experience`` |
    | Interests       | 0.10   | Bio/headline keyword overlap with project description |
    | Availability    | 0.10   | ``user.open_to_work`` |
    | Contributions   | 0.10   | Owned projects + accepted applications (log scale) |
    | Network         | 0.05   | Mutual-follower social boost |

    Results are cached for 10 minutes.

    Args:
        project_id (None | Unset | UUID): Optional project ID. When supplied, builders are ranked
            against that project's required skills, tech stack and minimum experience. When omitted,
            builders are ranked against the requester's own profile (find-collaborators mode).
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecommendationResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: None | Unset | UUID = UNSET,
    limit: int | Unset = 20,
) -> HTTPValidationError | RecommendationResponse | None:
    """Get recommended builders (collaborators)

     Returns a ranked list of recommended builders (potential collaborators).

    **Scoring factors** (each in ``[0, 1]``):

    | Factor          | Weight | Source |
    | --------------- | ------ | ------ |
    | Skills          | 0.30   | Jaccard overlap weighted by skill level |
    | Technologies   | 0.20   | Builder skills vs. ``project.tech_stack`` |
    | Experience      | 0.15   | Builder years vs. ``project_skill.minimum_experience`` |
    | Interests       | 0.10   | Bio/headline keyword overlap with project description |
    | Availability    | 0.10   | ``user.open_to_work`` |
    | Contributions   | 0.10   | Owned projects + accepted applications (log scale) |
    | Network         | 0.05   | Mutual-follower social boost |

    Results are cached for 10 minutes.

    Args:
        project_id (None | Unset | UUID): Optional project ID. When supplied, builders are ranked
            against that project's required skills, tech stack and minimum experience. When omitted,
            builders are ranked against the requester's own profile (find-collaborators mode).
        limit (int | Unset):  Default: 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecommendationResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
            limit=limit,
        )
    ).parsed
