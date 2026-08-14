from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_response import ProjectResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
    language: None | str | Unset = UNSET,
    experience: None | str | Unset = UNSET,
    remote: bool | None | Unset = UNSET,
    paid: bool | None | Unset = UNSET,
    opensource: bool | None | Unset = UNSET,
    tech: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    json_language: None | str | Unset
    if isinstance(language, Unset):
        json_language = UNSET
    else:
        json_language = language
    params["language"] = json_language

    json_experience: None | str | Unset
    if isinstance(experience, Unset):
        json_experience = UNSET
    else:
        json_experience = experience
    params["experience"] = json_experience

    json_remote: bool | None | Unset
    if isinstance(remote, Unset):
        json_remote = UNSET
    else:
        json_remote = remote
    params["remote"] = json_remote

    json_paid: bool | None | Unset
    if isinstance(paid, Unset):
        json_paid = UNSET
    else:
        json_paid = paid
    params["paid"] = json_paid

    json_opensource: bool | None | Unset
    if isinstance(opensource, Unset):
        json_opensource = UNSET
    else:
        json_opensource = opensource
    params["opensource"] = json_opensource

    json_tech: None | str | Unset
    if isinstance(tech, Unset):
        json_tech = UNSET
    else:
        json_tech = tech
    params["tech"] = json_tech

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/projects/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ProjectResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectResponse.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[ProjectResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
    language: None | str | Unset = UNSET,
    experience: None | str | Unset = UNSET,
    remote: bool | None | Unset = UNSET,
    paid: bool | None | Unset = UNSET,
    opensource: bool | None | Unset = UNSET,
    tech: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[ProjectResponse]]:
    """List Projects

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.
        language (None | str | Unset):
        experience (None | str | Unset):
        remote (bool | None | Unset):
        paid (bool | None | Unset):
        opensource (bool | None | Unset):
        tech (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ProjectResponse]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        language=language,
        experience=experience,
        remote=remote,
        paid=paid,
        opensource=opensource,
        tech=tech,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
    language: None | str | Unset = UNSET,
    experience: None | str | Unset = UNSET,
    remote: bool | None | Unset = UNSET,
    paid: bool | None | Unset = UNSET,
    opensource: bool | None | Unset = UNSET,
    tech: None | str | Unset = UNSET,
) -> HTTPValidationError | list[ProjectResponse] | None:
    """List Projects

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.
        language (None | str | Unset):
        experience (None | str | Unset):
        remote (bool | None | Unset):
        paid (bool | None | Unset):
        opensource (bool | None | Unset):
        tech (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ProjectResponse]
    """

    return sync_detailed(
        client=client,
        skip=skip,
        limit=limit,
        language=language,
        experience=experience,
        remote=remote,
        paid=paid,
        opensource=opensource,
        tech=tech,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
    language: None | str | Unset = UNSET,
    experience: None | str | Unset = UNSET,
    remote: bool | None | Unset = UNSET,
    paid: bool | None | Unset = UNSET,
    opensource: bool | None | Unset = UNSET,
    tech: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[ProjectResponse]]:
    """List Projects

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.
        language (None | str | Unset):
        experience (None | str | Unset):
        remote (bool | None | Unset):
        paid (bool | None | Unset):
        opensource (bool | None | Unset):
        tech (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ProjectResponse]]
    """

    kwargs = _get_kwargs(
        skip=skip,
        limit=limit,
        language=language,
        experience=experience,
        remote=remote,
        paid=paid,
        opensource=opensource,
        tech=tech,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 20,
    language: None | str | Unset = UNSET,
    experience: None | str | Unset = UNSET,
    remote: bool | None | Unset = UNSET,
    paid: bool | None | Unset = UNSET,
    opensource: bool | None | Unset = UNSET,
    tech: None | str | Unset = UNSET,
) -> HTTPValidationError | list[ProjectResponse] | None:
    """List Projects

    Args:
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 20.
        language (None | str | Unset):
        experience (None | str | Unset):
        remote (bool | None | Unset):
        paid (bool | None | Unset):
        opensource (bool | None | Unset):
        tech (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ProjectResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            skip=skip,
            limit=limit,
            language=language,
            experience=experience,
            remote=remote,
            paid=paid,
            opensource=opensource,
            tech=tech,
        )
    ).parsed
