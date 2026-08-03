from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RepositoryInfo")


@_attrs_define
class RepositoryInfo:
    """Basic metadata about the analyzed repository.

    Attributes:
        stars (int | Unset):  Default: 0.
        forks (int | Unset):  Default: 0.
        open_issues (int | Unset):  Default: 0.
        language (None | str | Unset):
        description (None | str | Unset):
        default_branch (str | Unset):  Default: 'main'.
        last_push (None | str | Unset):
        topics (list[str] | Unset):
    """

    stars: int | Unset = 0
    forks: int | Unset = 0
    open_issues: int | Unset = 0
    language: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    default_branch: str | Unset = "main"
    last_push: None | str | Unset = UNSET
    topics: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stars = self.stars

        forks = self.forks

        open_issues = self.open_issues

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        default_branch = self.default_branch

        last_push: None | str | Unset
        if isinstance(self.last_push, Unset):
            last_push = UNSET
        else:
            last_push = self.last_push

        topics: list[str] | Unset = UNSET
        if not isinstance(self.topics, Unset):
            topics = self.topics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stars is not UNSET:
            field_dict["stars"] = stars
        if forks is not UNSET:
            field_dict["forks"] = forks
        if open_issues is not UNSET:
            field_dict["open_issues"] = open_issues
        if language is not UNSET:
            field_dict["language"] = language
        if description is not UNSET:
            field_dict["description"] = description
        if default_branch is not UNSET:
            field_dict["default_branch"] = default_branch
        if last_push is not UNSET:
            field_dict["last_push"] = last_push
        if topics is not UNSET:
            field_dict["topics"] = topics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stars = d.pop("stars", UNSET)

        forks = d.pop("forks", UNSET)

        open_issues = d.pop("open_issues", UNSET)

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        default_branch = d.pop("default_branch", UNSET)

        def _parse_last_push(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_push = _parse_last_push(d.pop("last_push", UNSET))

        topics = cast(list[str], d.pop("topics", UNSET))

        repository_info = cls(
            stars=stars,
            forks=forks,
            open_issues=open_issues,
            language=language,
            description=description,
            default_branch=default_branch,
            last_push=last_push,
            topics=topics,
        )

        repository_info.additional_properties = d
        return repository_info

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
