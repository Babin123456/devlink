from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_action import AuditAction
from ...models.audit_log_response import AuditLogResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    actor_id: None | Unset | UUID = UNSET,
    project_id: None | Unset | UUID = UNSET,
    organization_id: None | Unset | UUID = UNSET,
    action: AuditAction | None | Unset = UNSET,
    entity_type: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    json_actor_id: None | str | Unset
    if isinstance(actor_id, Unset):
        json_actor_id = UNSET
    elif isinstance(actor_id, UUID):
        json_actor_id = str(actor_id)
    else:
        json_actor_id = actor_id
    params["actor_id"] = json_actor_id

    json_project_id: None | str | Unset
    if isinstance(project_id, Unset):
        json_project_id = UNSET
    elif isinstance(project_id, UUID):
        json_project_id = str(project_id)
    else:
        json_project_id = project_id
    params["project_id"] = json_project_id

    json_organization_id: None | str | Unset
    if isinstance(organization_id, Unset):
        json_organization_id = UNSET
    elif isinstance(organization_id, UUID):
        json_organization_id = str(organization_id)
    else:
        json_organization_id = organization_id
    params["organization_id"] = json_organization_id

    json_action: None | str | Unset
    if isinstance(action, Unset):
        json_action = UNSET
    elif isinstance(action, AuditAction):
        json_action = action.value
    else:
        json_action = action
    params["action"] = json_action

    json_entity_type: None | str | Unset
    if isinstance(entity_type, Unset):
        json_entity_type = UNSET
    else:
        json_entity_type = entity_type
    params["entity_type"] = json_entity_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/audit/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[AuditLogResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AuditLogResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[AuditLogResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    actor_id: None | Unset | UUID = UNSET,
    project_id: None | Unset | UUID = UNSET,
    organization_id: None | Unset | UUID = UNSET,
    action: AuditAction | None | Unset = UNSET,
    entity_type: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[AuditLogResponse]]:
    """Get Audit Logs

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        actor_id (None | Unset | UUID):
        project_id (None | Unset | UUID):
        organization_id (None | Unset | UUID):
        action (AuditAction | None | Unset):
        entity_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AuditLogResponse]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        actor_id=actor_id,
        project_id=project_id,
        organization_id=organization_id,
        action=action,
        entity_type=entity_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    actor_id: None | Unset | UUID = UNSET,
    project_id: None | Unset | UUID = UNSET,
    organization_id: None | Unset | UUID = UNSET,
    action: AuditAction | None | Unset = UNSET,
    entity_type: None | str | Unset = UNSET,
) -> HTTPValidationError | list[AuditLogResponse] | None:
    """Get Audit Logs

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        actor_id (None | Unset | UUID):
        project_id (None | Unset | UUID):
        organization_id (None | Unset | UUID):
        action (AuditAction | None | Unset):
        entity_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AuditLogResponse]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        actor_id=actor_id,
        project_id=project_id,
        organization_id=organization_id,
        action=action,
        entity_type=entity_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    actor_id: None | Unset | UUID = UNSET,
    project_id: None | Unset | UUID = UNSET,
    organization_id: None | Unset | UUID = UNSET,
    action: AuditAction | None | Unset = UNSET,
    entity_type: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[AuditLogResponse]]:
    """Get Audit Logs

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        actor_id (None | Unset | UUID):
        project_id (None | Unset | UUID):
        organization_id (None | Unset | UUID):
        action (AuditAction | None | Unset):
        entity_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AuditLogResponse]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        actor_id=actor_id,
        project_id=project_id,
        organization_id=organization_id,
        action=action,
        entity_type=entity_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    actor_id: None | Unset | UUID = UNSET,
    project_id: None | Unset | UUID = UNSET,
    organization_id: None | Unset | UUID = UNSET,
    action: AuditAction | None | Unset = UNSET,
    entity_type: None | str | Unset = UNSET,
) -> HTTPValidationError | list[AuditLogResponse] | None:
    """Get Audit Logs

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        actor_id (None | Unset | UUID):
        project_id (None | Unset | UUID):
        organization_id (None | Unset | UUID):
        action (AuditAction | None | Unset):
        entity_type (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AuditLogResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            actor_id=actor_id,
            project_id=project_id,
            organization_id=organization_id,
            action=action,
            entity_type=entity_type,
        )
    ).parsed
