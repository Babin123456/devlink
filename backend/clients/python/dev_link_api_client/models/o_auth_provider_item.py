from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OAuthProviderItem")


@_attrs_define
class OAuthProviderItem:
    """
    Attributes:
        provider (str):
        is_linked (bool):
        provider_user_id (None | str | Unset):
    """

    provider: str
    is_linked: bool
    provider_user_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        is_linked = self.is_linked

        provider_user_id: None | str | Unset
        if isinstance(self.provider_user_id, Unset):
            provider_user_id = UNSET
        else:
            provider_user_id = self.provider_user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "is_linked": is_linked,
            }
        )
        if provider_user_id is not UNSET:
            field_dict["provider_user_id"] = provider_user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = d.pop("provider")

        is_linked = d.pop("is_linked")

        def _parse_provider_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        provider_user_id = _parse_provider_user_id(d.pop("provider_user_id", UNSET))

        o_auth_provider_item = cls(
            provider=provider,
            is_linked=is_linked,
            provider_user_id=provider_user_id,
        )

        o_auth_provider_item.additional_properties = d
        return o_auth_provider_item

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
