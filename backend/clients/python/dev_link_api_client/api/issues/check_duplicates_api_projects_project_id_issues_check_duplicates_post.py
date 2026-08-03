from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.duplicate_check_request import DuplicateCheckRequest
from ...models.duplicate_check_response import DuplicateCheckResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    project_id: UUID,
    *,
    body: DuplicateCheckRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/projects/{project_id}/issues/check-duplicates".format(
            project_id=quote(str(project_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DuplicateCheckResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DuplicateCheckResponse.from_dict(response.json())

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
) -> Response[DuplicateCheckResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: DuplicateCheckRequest,
) -> Response[DuplicateCheckResponse | HTTPValidationError]:
    """Check Duplicates

     Check for duplicate issues before creating a new one.

    Uses AI embeddings to find semantically similar issues
    within the same project.

    Args:
        project_id (UUID):
        body (DuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DuplicateCheckResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: DuplicateCheckRequest,
) -> DuplicateCheckResponse | HTTPValidationError | None:
    """Check Duplicates

     Check for duplicate issues before creating a new one.

    Uses AI embeddings to find semantically similar issues
    within the same project.

    Args:
        project_id (UUID):
        body (DuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DuplicateCheckResponse | HTTPValidationError
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: DuplicateCheckRequest,
) -> Response[DuplicateCheckResponse | HTTPValidationError]:
    """Check Duplicates

     Check for duplicate issues before creating a new one.

    Uses AI embeddings to find semantically similar issues
    within the same project.

    Args:
        project_id (UUID):
        body (DuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DuplicateCheckResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    body: DuplicateCheckRequest,
) -> DuplicateCheckResponse | HTTPValidationError | None:
    """Check Duplicates

     Check for duplicate issues before creating a new one.

    Uses AI embeddings to find semantically similar issues
    within the same project.

    Args:
        project_id (UUID):
        body (DuplicateCheckRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DuplicateCheckResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
        )
    ).parsed
