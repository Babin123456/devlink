from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.repository_provider import RepositoryProvider
from ..types import UNSET, Unset

T = TypeVar("T", bound="RepositoryUpdate")


@_attrs_define
class RepositoryUpdate:
    """
    Attributes:
        provider (None | RepositoryProvider | Unset):
        repository_id (None | str | Unset):
        owner (None | str | Unset):
        name (None | str | Unset):
        full_name (None | str | Unset):
        description (None | str | Unset):
        default_branch (None | str | Unset):
        clone_url (None | str | Unset):
        html_url (None | str | Unset):
        homepage (None | str | Unset):
        language (None | str | Unset):
        stars (int | None | Unset):
        forks (int | None | Unset):
        watchers (int | None | Unset):
        open_issues (int | None | Unset):
        contributors (int | None | Unset):
        is_private (bool | None | Unset):
        archived (bool | None | Unset):
        synced (bool | None | Unset):
    """

    provider: None | RepositoryProvider | Unset = UNSET
    repository_id: None | str | Unset = UNSET
    owner: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    full_name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    default_branch: None | str | Unset = UNSET
    clone_url: None | str | Unset = UNSET
    html_url: None | str | Unset = UNSET
    homepage: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    stars: int | None | Unset = UNSET
    forks: int | None | Unset = UNSET
    watchers: int | None | Unset = UNSET
    open_issues: int | None | Unset = UNSET
    contributors: int | None | Unset = UNSET
    is_private: bool | None | Unset = UNSET
    archived: bool | None | Unset = UNSET
    synced: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider: None | str | Unset
        if isinstance(self.provider, Unset):
            provider = UNSET
        elif isinstance(self.provider, RepositoryProvider):
            provider = self.provider.value
        else:
            provider = self.provider

        repository_id: None | str | Unset
        if isinstance(self.repository_id, Unset):
            repository_id = UNSET
        else:
            repository_id = self.repository_id

        owner: None | str | Unset
        if isinstance(self.owner, Unset):
            owner = UNSET
        else:
            owner = self.owner

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        full_name: None | str | Unset
        if isinstance(self.full_name, Unset):
            full_name = UNSET
        else:
            full_name = self.full_name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        default_branch: None | str | Unset
        if isinstance(self.default_branch, Unset):
            default_branch = UNSET
        else:
            default_branch = self.default_branch

        clone_url: None | str | Unset
        if isinstance(self.clone_url, Unset):
            clone_url = UNSET
        else:
            clone_url = self.clone_url

        html_url: None | str | Unset
        if isinstance(self.html_url, Unset):
            html_url = UNSET
        else:
            html_url = self.html_url

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

        stars: int | None | Unset
        if isinstance(self.stars, Unset):
            stars = UNSET
        else:
            stars = self.stars

        forks: int | None | Unset
        if isinstance(self.forks, Unset):
            forks = UNSET
        else:
            forks = self.forks

        watchers: int | None | Unset
        if isinstance(self.watchers, Unset):
            watchers = UNSET
        else:
            watchers = self.watchers

        open_issues: int | None | Unset
        if isinstance(self.open_issues, Unset):
            open_issues = UNSET
        else:
            open_issues = self.open_issues

        contributors: int | None | Unset
        if isinstance(self.contributors, Unset):
            contributors = UNSET
        else:
            contributors = self.contributors

        is_private: bool | None | Unset
        if isinstance(self.is_private, Unset):
            is_private = UNSET
        else:
            is_private = self.is_private

        archived: bool | None | Unset
        if isinstance(self.archived, Unset):
            archived = UNSET
        else:
            archived = self.archived

        synced: bool | None | Unset
        if isinstance(self.synced, Unset):
            synced = UNSET
        else:
            synced = self.synced

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider is not UNSET:
            field_dict["provider"] = provider
        if repository_id is not UNSET:
            field_dict["repository_id"] = repository_id
        if owner is not UNSET:
            field_dict["owner"] = owner
        if name is not UNSET:
            field_dict["name"] = name
        if full_name is not UNSET:
            field_dict["full_name"] = full_name
        if description is not UNSET:
            field_dict["description"] = description
        if default_branch is not UNSET:
            field_dict["default_branch"] = default_branch
        if clone_url is not UNSET:
            field_dict["clone_url"] = clone_url
        if html_url is not UNSET:
            field_dict["html_url"] = html_url
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
        if synced is not UNSET:
            field_dict["synced"] = synced

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_provider(data: object) -> None | RepositoryProvider | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provider_type_0 = RepositoryProvider(data)

                return provider_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RepositoryProvider | Unset, data)

        provider = _parse_provider(d.pop("provider", UNSET))

        def _parse_repository_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        repository_id = _parse_repository_id(d.pop("repository_id", UNSET))

        def _parse_owner(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        owner = _parse_owner(d.pop("owner", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_full_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        full_name = _parse_full_name(d.pop("full_name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_default_branch(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_branch = _parse_default_branch(d.pop("default_branch", UNSET))

        def _parse_clone_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        clone_url = _parse_clone_url(d.pop("clone_url", UNSET))

        def _parse_html_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        html_url = _parse_html_url(d.pop("html_url", UNSET))

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

        def _parse_stars(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        stars = _parse_stars(d.pop("stars", UNSET))

        def _parse_forks(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        forks = _parse_forks(d.pop("forks", UNSET))

        def _parse_watchers(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        watchers = _parse_watchers(d.pop("watchers", UNSET))

        def _parse_open_issues(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        open_issues = _parse_open_issues(d.pop("open_issues", UNSET))

        def _parse_contributors(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        contributors = _parse_contributors(d.pop("contributors", UNSET))

        def _parse_is_private(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_private = _parse_is_private(d.pop("is_private", UNSET))

        def _parse_archived(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        archived = _parse_archived(d.pop("archived", UNSET))

        def _parse_synced(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        synced = _parse_synced(d.pop("synced", UNSET))

        repository_update = cls(
            provider=provider,
            repository_id=repository_id,
            owner=owner,
            name=name,
            full_name=full_name,
            description=description,
            default_branch=default_branch,
            clone_url=clone_url,
            html_url=html_url,
            homepage=homepage,
            language=language,
            stars=stars,
            forks=forks,
            watchers=watchers,
            open_issues=open_issues,
            contributors=contributors,
            is_private=is_private,
            archived=archived,
            synced=synced,
        )

        repository_update.additional_properties = d
        return repository_update

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
