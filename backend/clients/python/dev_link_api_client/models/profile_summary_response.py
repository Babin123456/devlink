from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProfileSummaryResponse")


@_attrs_define
class ProfileSummaryResponse:
    """Response containing the generated profile summary.

    Attributes:
        summary (str): Generated professional profile summary
        user_id (UUID):
        user_name (str):
    """

    summary: str
    user_id: UUID
    user_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary = self.summary

        user_id = str(self.user_id)

        user_name = self.user_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "user_id": user_id,
                "user_name": user_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        summary = d.pop("summary")

        user_id = UUID(d.pop("user_id"))

        user_name = d.pop("user_name")

        profile_summary_response = cls(
            summary=summary,
            user_id=user_id,
            user_name=user_name,
        )

        profile_summary_response.additional_properties = d
        return profile_summary_response

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
