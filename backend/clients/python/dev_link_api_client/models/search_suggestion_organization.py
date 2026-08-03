from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchSuggestionOrganization")


@_attrs_define
class SearchSuggestionOrganization:
    """
    Attributes:
        id (UUID):
        name (str):
        slug (str):
        logo_url (None | str | Unset):
        organization_type (None | str | Unset):
        verified (bool | Unset):  Default: False.
    """

    id: UUID
    name: str
    slug: str
    logo_url: None | str | Unset = UNSET
    organization_type: None | str | Unset = UNSET
    verified: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        slug = self.slug

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        organization_type: None | str | Unset
        if isinstance(self.organization_type, Unset):
            organization_type = UNSET
        else:
            organization_type = self.organization_type

        verified = self.verified

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "slug": slug,
            }
        )
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if organization_type is not UNSET:
            field_dict["organization_type"] = organization_type
        if verified is not UNSET:
            field_dict["verified"] = verified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logo_url", UNSET))

        def _parse_organization_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        organization_type = _parse_organization_type(d.pop("organization_type", UNSET))

        verified = d.pop("verified", UNSET)

        search_suggestion_organization = cls(
            id=id,
            name=name,
            slug=slug,
            logo_url=logo_url,
            organization_type=organization_type,
            verified=verified,
        )

        search_suggestion_organization.additional_properties = d
        return search_suggestion_organization

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
