from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FollowStatusResponse")


@_attrs_define
class FollowStatusResponse:
    """
    Attributes:
        is_following (bool):
        follower_count (int):
        following_count (int):
    """

    is_following: bool
    follower_count: int
    following_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_following = self.is_following

        follower_count = self.follower_count

        following_count = self.following_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_following": is_following,
                "follower_count": follower_count,
                "following_count": following_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_following = d.pop("is_following")

        follower_count = d.pop("follower_count")

        following_count = d.pop("following_count")

        follow_status_response = cls(
            is_following=is_following,
            follower_count=follower_count,
            following_count=following_count,
        )

        follow_status_response.additional_properties = d
        return follow_status_response

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
