from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_org_audit_log_request import CreateOrgAuditLogRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.org_audit_log_response import OrgAuditLogResponse
from ...types import Response


def _get_kwargs(
    org_id: UUID,
    *,
    body: CreateOrgAuditLogRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/organizations/{org_id}/audit-logs".format(
            org_id=quote(str(org_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | OrgAuditLogResponse | None:
    if response.status_code == 201:
        response_201 = OrgAuditLogResponse.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | OrgAuditLogResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrgAuditLogRequest,
) -> Response[HTTPValidationError | OrgAuditLogResponse]:
    """Create immutable organization audit log record

     Record an immutable organization audit event.

    Args:
        org_id (UUID):
        body (CreateOrgAuditLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OrgAuditLogResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrgAuditLogRequest,
) -> HTTPValidationError | OrgAuditLogResponse | None:
    """Create immutable organization audit log record

     Record an immutable organization audit event.

    Args:
        org_id (UUID):
        body (CreateOrgAuditLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OrgAuditLogResponse
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    org_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrgAuditLogRequest,
) -> Response[HTTPValidationError | OrgAuditLogResponse]:
    """Create immutable organization audit log record

     Record an immutable organization audit event.

    Args:
        org_id (UUID):
        body (CreateOrgAuditLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OrgAuditLogResponse]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateOrgAuditLogRequest,
) -> HTTPValidationError | OrgAuditLogResponse | None:
    """Create immutable organization audit log record

     Record an immutable organization audit event.

    Args:
        org_id (UUID):
        body (CreateOrgAuditLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OrgAuditLogResponse
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
            body=body,
        )
    ).parsed
