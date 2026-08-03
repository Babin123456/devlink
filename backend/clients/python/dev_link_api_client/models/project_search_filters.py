from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectSearchFilters")


@_attrs_define
class ProjectSearchFilters:
    """Represents the filterable fields on a project search.

    Attributes:
        q (None | str | Unset):
        stage (None | str | Unset):
        language (None | str | Unset):
        experience (None | str | Unset):
        is_remote (bool | None | Unset):
        is_paid (bool | None | Unset):
        is_open_source (bool | None | Unset):
        tags (list[str] | None | Unset):
        hiring (bool | None | Unset):
    """

    q: None | str | Unset = UNSET
    stage: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    experience: None | str | Unset = UNSET
    is_remote: bool | None | Unset = UNSET
    is_paid: bool | None | Unset = UNSET
    is_open_source: bool | None | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    hiring: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        q: None | str | Unset
        if isinstance(self.q, Unset):
            q = UNSET
        else:
            q = self.q

        stage: None | str | Unset
        if isinstance(self.stage, Unset):
            stage = UNSET
        else:
            stage = self.stage

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        experience: None | str | Unset
        if isinstance(self.experience, Unset):
            experience = UNSET
        else:
            experience = self.experience

        is_remote: bool | None | Unset
        if isinstance(self.is_remote, Unset):
            is_remote = UNSET
        else:
            is_remote = self.is_remote

        is_paid: bool | None | Unset
        if isinstance(self.is_paid, Unset):
            is_paid = UNSET
        else:
            is_paid = self.is_paid

        is_open_source: bool | None | Unset
        if isinstance(self.is_open_source, Unset):
            is_open_source = UNSET
        else:
            is_open_source = self.is_open_source

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        hiring: bool | None | Unset
        if isinstance(self.hiring, Unset):
            hiring = UNSET
        else:
            hiring = self.hiring

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if q is not UNSET:
            field_dict["q"] = q
        if stage is not UNSET:
            field_dict["stage"] = stage
        if language is not UNSET:
            field_dict["language"] = language
        if experience is not UNSET:
            field_dict["experience"] = experience
        if is_remote is not UNSET:
            field_dict["is_remote"] = is_remote
        if is_paid is not UNSET:
            field_dict["is_paid"] = is_paid
        if is_open_source is not UNSET:
            field_dict["is_open_source"] = is_open_source
        if tags is not UNSET:
            field_dict["tags"] = tags
        if hiring is not UNSET:
            field_dict["hiring"] = hiring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_q(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        q = _parse_q(d.pop("q", UNSET))

        def _parse_stage(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        stage = _parse_stage(d.pop("stage", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_experience(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience = _parse_experience(d.pop("experience", UNSET))

        def _parse_is_remote(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_remote = _parse_is_remote(d.pop("is_remote", UNSET))

        def _parse_is_paid(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_paid = _parse_is_paid(d.pop("is_paid", UNSET))

        def _parse_is_open_source(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_open_source = _parse_is_open_source(d.pop("is_open_source", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_hiring(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        hiring = _parse_hiring(d.pop("hiring", UNSET))

        project_search_filters = cls(
            q=q,
            stage=stage,
            language=language,
            experience=experience,
            is_remote=is_remote,
            is_paid=is_paid,
            is_open_source=is_open_source,
            tags=tags,
            hiring=hiring,
        )

        project_search_filters.additional_properties = d
        return project_search_filters

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
