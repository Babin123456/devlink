from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BlockStatusResponse")


@_attrs_define
class BlockStatusResponse:
    """
    Attributes:
        is_blocked_by_me (bool): Whether the current user has blocked the target user
        is_blocking_me (bool): Whether the target user has blocked the current user
        has_block_relationship (bool): Whether either user has blocked the other
    """

    is_blocked_by_me: bool
    is_blocking_me: bool
    has_block_relationship: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_blocked_by_me = self.is_blocked_by_me

        is_blocking_me = self.is_blocking_me

        has_block_relationship = self.has_block_relationship

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_blocked_by_me": is_blocked_by_me,
                "is_blocking_me": is_blocking_me,
                "has_block_relationship": has_block_relationship,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_blocked_by_me = d.pop("is_blocked_by_me")

        is_blocking_me = d.pop("is_blocking_me")

        has_block_relationship = d.pop("has_block_relationship")

        block_status_response = cls(
            is_blocked_by_me=is_blocked_by_me,
            is_blocking_me=is_blocking_me,
            has_block_relationship=has_block_relationship,
        )

        block_status_response.additional_properties = d
        return block_status_response

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
