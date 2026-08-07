from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.repository_provider import RepositoryProvider
from ..types import UNSET, Unset

T = TypeVar("T", bound="RepositoryResponse")


@_attrs_define
class RepositoryResponse:
    """
    Attributes:
        provider (RepositoryProvider):
        owner (str):
        name (str):
        full_name (str):
        html_url (str):
        id (UUID):
        project_id (UUID):
        synced (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        repository_id (None | str | Unset):
        description (None | str | Unset):
        default_branch (str | Unset):  Default: 'main'.
        clone_url (None | str | Unset):
        homepage (None | str | Unset):
        language (None | str | Unset):
        stars (int | Unset):  Default: 0.
        forks (int | Unset):  Default: 0.
        watchers (int | Unset):  Default: 0.
        open_issues (int | Unset):  Default: 0.
        contributors (int | Unset):  Default: 0.
        is_private (bool | Unset):  Default: False.
        archived (bool | Unset):  Default: False.
        connected_by (None | Unset | UUID):
        last_synced_at (datetime.datetime | None | Unset):
    """

    provider: RepositoryProvider
    owner: str
    name: str
    full_name: str
    html_url: str
    id: UUID
    project_id: UUID
    synced: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    repository_id: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    default_branch: str | Unset = "main"
    clone_url: None | str | Unset = UNSET
    homepage: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    stars: int | Unset = 0
    forks: int | Unset = 0
    watchers: int | Unset = 0
    open_issues: int | Unset = 0
    contributors: int | Unset = 0
    is_private: bool | Unset = False
    archived: bool | Unset = False
    connected_by: None | Unset | UUID = UNSET
    last_synced_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider.value

        owner = self.owner

        name = self.name

        full_name = self.full_name

        html_url = self.html_url

        id = str(self.id)

        project_id = str(self.project_id)

        synced = self.synced

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        repository_id: None | str | Unset
        if isinstance(self.repository_id, Unset):
            repository_id = UNSET
        else:
            repository_id = self.repository_id

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        default_branch = self.default_branch

        clone_url: None | str | Unset
        if isinstance(self.clone_url, Unset):
            clone_url = UNSET
        else:
            clone_url = self.clone_url

        homepage: None | str | Unset
        if isinstance(self.homepage, Unset):
            homepage = UNSET
        else:
            homepage = self.homepage

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        stars = self.stars

        forks = self.forks

        watchers = self.watchers

        open_issues = self.open_issues

        contributors = self.contributors

        is_private = self.is_private

        archived = self.archived

        connected_by: None | str | Unset
        if isinstance(self.connected_by, Unset):
            connected_by = UNSET
        elif isinstance(self.connected_by, UUID):
            connected_by = str(self.connected_by)
        else:
            connected_by = self.connected_by

        last_synced_at: None | str | Unset
        if isinstance(self.last_synced_at, Unset):
            last_synced_at = UNSET
        elif isinstance(self.last_synced_at, datetime.datetime):
            last_synced_at = self.last_synced_at.isoformat()
        else:
            last_synced_at = self.last_synced_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "owner": owner,
                "name": name,
                "full_name": full_name,
                "html_url": html_url,
                "id": id,
                "project_id": project_id,
                "synced": synced,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if repository_id is not UNSET:
            field_dict["repository_id"] = repository_id
        if description is not UNSET:
            field_dict["description"] = description
        if default_branch is not UNSET:
            field_dict["default_branch"] = default_branch
        if clone_url is not UNSET:
            field_dict["clone_url"] = clone_url
        if homepage is not UNSET:
            field_dict["homepage"] = homepage
        if language is not UNSET:
            field_dict["language"] = language
        if stars is not UNSET:
            field_dict["stars"] = stars
        if forks is not UNSET:
            field_dict["forks"] = forks
        if watchers is not UNSET:
            field_dict["watchers"] = watchers
        if open_issues is not UNSET:
            field_dict["open_issues"] = open_issues
        if contributors is not UNSET:
            field_dict["contributors"] = contributors
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if archived is not UNSET:
            field_dict["archived"] = archived
        if connected_by is not UNSET:
            field_dict["connected_by"] = connected_by
        if last_synced_at is not UNSET:
            field_dict["last_synced_at"] = last_synced_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = RepositoryProvider(d.pop("provider"))

        owner = d.pop("owner")

        name = d.pop("name")

        full_name = d.pop("full_name")

        html_url = d.pop("html_url")

        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        synced = d.pop("synced")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_repository_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        repository_id = _parse_repository_id(d.pop("repository_id", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        default_branch = d.pop("default_branch", UNSET)

        def _parse_clone_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        clone_url = _parse_clone_url(d.pop("clone_url", UNSET))

        def _parse_homepage(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        homepage = _parse_homepage(d.pop("homepage", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        stars = d.pop("stars", UNSET)

        forks = d.pop("forks", UNSET)

        watchers = d.pop("watchers", UNSET)

        open_issues = d.pop("open_issues", UNSET)

        contributors = d.pop("contributors", UNSET)

        is_private = d.pop("is_private", UNSET)

        archived = d.pop("archived", UNSET)

        def _parse_connected_by(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                connected_by_type_0 = UUID(data)

                return connected_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        connected_by = _parse_connected_by(d.pop("connected_by", UNSET))

        def _parse_last_synced_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_synced_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_synced_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_synced_at = _parse_last_synced_at(d.pop("last_synced_at", UNSET))

        repository_response = cls(
            provider=provider,
            owner=owner,
            name=name,
            full_name=full_name,
            html_url=html_url,
            id=id,
            project_id=project_id,
            synced=synced,
            created_at=created_at,
            updated_at=updated_at,
            repository_id=repository_id,
            description=description,
            default_branch=default_branch,
            clone_url=clone_url,
            homepage=homepage,
            language=language,
            stars=stars,
            forks=forks,
            watchers=watchers,
            open_issues=open_issues,
            contributors=contributors,
            is_private=is_private,
            archived=archived,
            connected_by=connected_by,
            last_synced_at=last_synced_at,
        )

        repository_response.additional_properties = d
        return repository_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
