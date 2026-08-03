from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.organization_type import OrganizationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationCreate")


@_attrs_define
class OrganizationCreate:
    """
    Attributes:
        name (str):
        slug (None | str | Unset): Unique URL slug. Generated automatically from name if omitted.
        description (None | str | Unset):
        organization_type (OrganizationType | Unset):
        website (None | str | Unset):
        email (None | str | Unset):
        phone (None | str | Unset):
        logo_url (None | str | Unset):
        banner_url (None | str | Unset):
        location (None | str | Unset):
        github_url (None | str | Unset):
        linkedin_url (None | str | Unset):
        twitter_url (None | str | Unset):
        hiring (bool | Unset):  Default: False.
    """

    name: str
    slug: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    organization_type: OrganizationType | Unset = UNSET
    website: None | str | Unset = UNSET
    email: None | str | Unset = UNSET
    phone: None | str | Unset = UNSET
    logo_url: None | str | Unset = UNSET
    banner_url: None | str | Unset = UNSET
    location: None | str | Unset = UNSET
    github_url: None | str | Unset = UNSET
    linkedin_url: None | str | Unset = UNSET
    twitter_url: None | str | Unset = UNSET
    hiring: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        slug: None | str | Unset
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        organization_type: str | Unset = UNSET
        if not isinstance(self.organization_type, Unset):
            organization_type = self.organization_type.value

        website: None | str | Unset
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        phone: None | str | Unset
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        banner_url: None | str | Unset
        if isinstance(self.banner_url, Unset):
            banner_url = UNSET
        else:
            banner_url = self.banner_url

        location: None | str | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        else:
            location = self.location

        github_url: None | str | Unset
        if isinstance(self.github_url, Unset):
            github_url = UNSET
        else:
            github_url = self.github_url

        linkedin_url: None | str | Unset
        if isinstance(self.linkedin_url, Unset):
            linkedin_url = UNSET
        else:
            linkedin_url = self.linkedin_url

        twitter_url: None | str | Unset
        if isinstance(self.twitter_url, Unset):
            twitter_url = UNSET
        else:
            twitter_url = self.twitter_url

        hiring = self.hiring

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if description is not UNSET:
            field_dict["description"] = description
        if organization_type is not UNSET:
            field_dict["organization_type"] = organization_type
        if website is not UNSET:
            field_dict["website"] = website
        if email is not UNSET:
            field_dict["email"] = email
        if phone is not UNSET:
            field_dict["phone"] = phone
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if banner_url is not UNSET:
            field_dict["banner_url"] = banner_url
        if location is not UNSET:
            field_dict["location"] = location
        if github_url is not UNSET:
            field_dict["github_url"] = github_url
        if linkedin_url is not UNSET:
            field_dict["linkedin_url"] = linkedin_url
        if twitter_url is not UNSET:
            field_dict["twitter_url"] = twitter_url
        if hiring is not UNSET:
            field_dict["hiring"] = hiring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_slug(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        slug = _parse_slug(d.pop("slug", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _organization_type = d.pop("organization_type", UNSET)
        organization_type: OrganizationType | Unset
        if isinstance(_organization_type, Unset):
            organization_type = UNSET
        else:
            organization_type = OrganizationType(_organization_type)

        def _parse_website(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        website = _parse_website(d.pop("website", UNSET))

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_phone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        phone = _parse_phone(d.pop("phone", UNSET))

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logo_url", UNSET))

        def _parse_banner_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        banner_url = _parse_banner_url(d.pop("banner_url", UNSET))

        def _parse_location(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_github_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        github_url = _parse_github_url(d.pop("github_url", UNSET))

        def _parse_linkedin_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        linkedin_url = _parse_linkedin_url(d.pop("linkedin_url", UNSET))

        def _parse_twitter_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        twitter_url = _parse_twitter_url(d.pop("twitter_url", UNSET))

        hiring = d.pop("hiring", UNSET)

        organization_create = cls(
            name=name,
            slug=slug,
            description=description,
            organization_type=organization_type,
            website=website,
            email=email,
            phone=phone,
            logo_url=logo_url,
            banner_url=banner_url,
            location=location,
            github_url=github_url,
            linkedin_url=linkedin_url,
            twitter_url=twitter_url,
            hiring=hiring,
        )

        organization_create.additional_properties = d
        return organization_create

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
