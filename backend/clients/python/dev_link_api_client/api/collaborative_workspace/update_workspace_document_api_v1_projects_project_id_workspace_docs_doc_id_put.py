from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_document_response import ProjectDocumentResponse
from ...models.project_document_update import ProjectDocumentUpdate
from ...types import Response


def _get_kwargs(
    project_id: UUID,
    doc_id: UUID,
    *,
    body: ProjectDocumentUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/projects/{project_id}/workspace/docs/{doc_id}".format(
            project_id=quote(str(project_id), safe=""),
            doc_id=quote(str(doc_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ProjectDocumentResponse | None:
    if response.status_code == 200:
        response_200 = ProjectDocumentResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ProjectDocumentResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    doc_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectDocumentUpdate,
) -> Response[HTTPValidationError | ProjectDocumentResponse]:
    """Update Workspace Document

    Args:
        project_id (UUID):
        doc_id (UUID):
        body (ProjectDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectDocumentResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        doc_id=doc_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    doc_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectDocumentUpdate,
) -> HTTPValidationError | ProjectDocumentResponse | None:
    """Update Workspace Document

    Args:
        project_id (UUID):
        doc_id (UUID):
        body (ProjectDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectDocumentResponse
    """

    return sync_detailed(
        project_id=project_id,
        doc_id=doc_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    doc_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectDocumentUpdate,
) -> Response[HTTPValidationError | ProjectDocumentResponse]:
    """Update Workspace Document

    Args:
        project_id (UUID):
        doc_id (UUID):
        body (ProjectDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ProjectDocumentResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        doc_id=doc_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    doc_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectDocumentUpdate,
) -> HTTPValidationError | ProjectDocumentResponse | None:
    """Update Workspace Document

    Args:
        project_id (UUID):
        doc_id (UUID):
        body (ProjectDocumentUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ProjectDocumentResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            doc_id=doc_id,
            client=client,
            body=body,
        )
    ).parsed
