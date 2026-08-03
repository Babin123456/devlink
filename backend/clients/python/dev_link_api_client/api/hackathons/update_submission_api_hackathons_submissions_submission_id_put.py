from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hackathon_submission_response import HackathonSubmissionResponse
from ...models.hackathon_submission_update import HackathonSubmissionUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    submission_id: UUID,
    *,
    body: HackathonSubmissionUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/hackathons/submissions/{submission_id}".format(
            submission_id=quote(str(submission_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | HackathonSubmissionResponse | None:
    if response.status_code == 200:
        response_200 = HackathonSubmissionResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | HackathonSubmissionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    submission_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonSubmissionUpdate,
) -> Response[HTTPValidationError | HackathonSubmissionResponse]:
    """Update Submission

    Args:
        submission_id (UUID):
        body (HackathonSubmissionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonSubmissionResponse]
    """

    kwargs = _get_kwargs(
        submission_id=submission_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    submission_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonSubmissionUpdate,
) -> HTTPValidationError | HackathonSubmissionResponse | None:
    """Update Submission

    Args:
        submission_id (UUID):
        body (HackathonSubmissionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonSubmissionResponse
    """

    return sync_detailed(
        submission_id=submission_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    submission_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonSubmissionUpdate,
) -> Response[HTTPValidationError | HackathonSubmissionResponse]:
    """Update Submission

    Args:
        submission_id (UUID):
        body (HackathonSubmissionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HackathonSubmissionResponse]
    """

    kwargs = _get_kwargs(
        submission_id=submission_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    submission_id: UUID,
    *,
    client: AuthenticatedClient,
    body: HackathonSubmissionUpdate,
) -> HTTPValidationError | HackathonSubmissionResponse | None:
    """Update Submission

    Args:
        submission_id (UUID):
        body (HackathonSubmissionUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HackathonSubmissionResponse
    """

    return (
        await asyncio_detailed(
            submission_id=submission_id,
            client=client,
            body=body,
        )
    ).parsed
