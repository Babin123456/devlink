from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.o_auth_provider_item import OAuthProviderItem


T = TypeVar("T", bound="OAuthProvidersListResponse")


@_attrs_define
class OAuthProvidersListResponse:
    """
    Attributes:
        has_password (bool):
        linked_count (int):
        providers (list[OAuthProviderItem]):
    """

    has_password: bool
    linked_count: int
    providers: list[OAuthProviderItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_password = self.has_password

        linked_count = self.linked_count

        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.to_dict()
            providers.append(providers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_password": has_password,
                "linked_count": linked_count,
                "providers": providers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.o_auth_provider_item import OAuthProviderItem

        d = dict(src_dict)
        has_password = d.pop("has_password")

        linked_count = d.pop("linked_count")

        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = OAuthProviderItem.from_dict(providers_item_data)

            providers.append(providers_item)

        o_auth_providers_list_response = cls(
            has_password=has_password,
            linked_count=linked_count,
            providers=providers,
        )

        o_auth_providers_list_response.additional_properties = d
        return o_auth_providers_list_response

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
