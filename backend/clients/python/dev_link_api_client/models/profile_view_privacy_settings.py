from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileViewPrivacySettings")


@_attrs_define
class ProfileViewPrivacySettings:
    """
    Attributes:
        hide_profile_views (bool | Unset): If True, your visits to other profiles will be recorded anonymously and
            hidden. Default: False.
    """

    hide_profile_views: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hide_profile_views = self.hide_profile_views

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if hide_profile_views is not UNSET:
            field_dict["hide_profile_views"] = hide_profile_views

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hide_profile_views = d.pop("hide_profile_views", UNSET)

        profile_view_privacy_settings = cls(
            hide_profile_views=hide_profile_views,
        )

        profile_view_privacy_settings.additional_properties = d
        return profile_view_privacy_settings

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
