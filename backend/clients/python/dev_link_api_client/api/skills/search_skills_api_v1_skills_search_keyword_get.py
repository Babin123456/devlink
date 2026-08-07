from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.skill_response import SkillResponse
from ...types import Response


def _get_kwargs(
    keyword: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/skills/search/{keyword}".format(
            keyword=quote(str(keyword), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[SkillResponse] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SkillResponse.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[SkillResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    keyword: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[SkillResponse]]:
    """Search Skills

    Args:
        keyword (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[SkillResponse]]
    """

    kwargs = _get_kwargs(
        keyword=keyword,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    keyword: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[SkillResponse] | None:
    """Search Skills

    Args:
        keyword (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[SkillResponse]
    """

    return sync_detailed(
        keyword=keyword,
        client=client,
    ).parsed


async def asyncio_detailed(
    keyword: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[SkillResponse]]:
    """Search Skills

    Args:
        keyword (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[SkillResponse]]
    """

    kwargs = _get_kwargs(
        keyword=keyword,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    keyword: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[SkillResponse] | None:
    """Search Skills

    Args:
        keyword (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[SkillResponse]
    """

    return (
        await asyncio_detailed(
            keyword=keyword,
            client=client,
        )
    ).parsed
