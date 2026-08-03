from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HackathonRegistrationCreate")


@_attrs_define
class HackathonRegistrationCreate:
    """
    Attributes:
        motivation (None | str | Unset):
        experience_level (None | str | Unset):
    """

    motivation: None | str | Unset = UNSET
    experience_level: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        motivation: None | str | Unset
        if isinstance(self.motivation, Unset):
            motivation = UNSET
        else:
            motivation = self.motivation

        experience_level: None | str | Unset
        if isinstance(self.experience_level, Unset):
            experience_level = UNSET
        else:
            experience_level = self.experience_level

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if motivation is not UNSET:
            field_dict["motivation"] = motivation
        if experience_level is not UNSET:
            field_dict["experience_level"] = experience_level

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_motivation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        motivation = _parse_motivation(d.pop("motivation", UNSET))

        def _parse_experience_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience_level = _parse_experience_level(d.pop("experience_level", UNSET))

        hackathon_registration_create = cls(
            motivation=motivation,
            experience_level=experience_level,
        )

        hackathon_registration_create.additional_properties = d
        return hackathon_registration_create

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
