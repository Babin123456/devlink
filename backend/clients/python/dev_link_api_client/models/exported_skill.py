from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportedSkill")


@_attrs_define
class ExportedSkill:
    """
    Attributes:
        id (UUID):
        name (str):
        level (None | str | Unset):
        years_of_experience (int | Unset):  Default: 0.
    """

    id: UUID
    name: str
    level: None | str | Unset = UNSET
    years_of_experience: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        level: None | str | Unset
        if isinstance(self.level, Unset):
            level = UNSET
        else:
            level = self.level

        years_of_experience = self.years_of_experience

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if level is not UNSET:
            field_dict["level"] = level
        if years_of_experience is not UNSET:
            field_dict["years_of_experience"] = years_of_experience

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        def _parse_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        level = _parse_level(d.pop("level", UNSET))

        years_of_experience = d.pop("years_of_experience", UNSET)

        exported_skill = cls(
            id=id,
            name=name,
            level=level,
            years_of_experience=years_of_experience,
        )

        exported_skill.additional_properties = d
        return exported_skill

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
