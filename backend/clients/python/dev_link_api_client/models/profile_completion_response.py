from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProfileCompletionResponse")


@_attrs_define
class ProfileCompletionResponse:
    """
    Attributes:
        completion (int): Profile completion percentage (0-100)
        missing (list[str]): List of missing profile factors
    """

    completion: int
    missing: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completion = self.completion

        missing = self.missing

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "completion": completion,
                "missing": missing,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        completion = d.pop("completion")

        missing = cast(list[str], d.pop("missing"))

        profile_completion_response = cls(
            completion=completion,
            missing=missing,
        )

        profile_completion_response.additional_properties = d
        return profile_completion_response

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
