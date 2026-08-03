from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.privacy_visibility import PrivacyVisibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="PrivacySettings")


@_attrs_define
class PrivacySettings:
    """
    Attributes:
        email (PrivacyVisibility | Unset):
        github (PrivacyVisibility | Unset):
        resume (PrivacyVisibility | Unset):
        social_links (PrivacyVisibility | Unset):
        availability (PrivacyVisibility | Unset):
    """

    email: PrivacyVisibility | Unset = UNSET
    github: PrivacyVisibility | Unset = UNSET
    resume: PrivacyVisibility | Unset = UNSET
    social_links: PrivacyVisibility | Unset = UNSET
    availability: PrivacyVisibility | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email: str | Unset = UNSET
        if not isinstance(self.email, Unset):
            email = self.email.value

        github: str | Unset = UNSET
        if not isinstance(self.github, Unset):
            github = self.github.value

        resume: str | Unset = UNSET
        if not isinstance(self.resume, Unset):
            resume = self.resume.value

        social_links: str | Unset = UNSET
        if not isinstance(self.social_links, Unset):
            social_links = self.social_links.value

        availability: str | Unset = UNSET
        if not isinstance(self.availability, Unset):
            availability = self.availability.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if github is not UNSET:
            field_dict["github"] = github
        if resume is not UNSET:
            field_dict["resume"] = resume
        if social_links is not UNSET:
            field_dict["social_links"] = social_links
        if availability is not UNSET:
            field_dict["availability"] = availability

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _email = d.pop("email", UNSET)
        email: PrivacyVisibility | Unset
        if isinstance(_email, Unset):
            email = UNSET
        else:
            email = PrivacyVisibility(_email)

        _github = d.pop("github", UNSET)
        github: PrivacyVisibility | Unset
        if isinstance(_github, Unset):
            github = UNSET
        else:
            github = PrivacyVisibility(_github)

        _resume = d.pop("resume", UNSET)
        resume: PrivacyVisibility | Unset
        if isinstance(_resume, Unset):
            resume = UNSET
        else:
            resume = PrivacyVisibility(_resume)

        _social_links = d.pop("social_links", UNSET)
        social_links: PrivacyVisibility | Unset
        if isinstance(_social_links, Unset):
            social_links = UNSET
        else:
            social_links = PrivacyVisibility(_social_links)

        _availability = d.pop("availability", UNSET)
        availability: PrivacyVisibility | Unset
        if isinstance(_availability, Unset):
            availability = UNSET
        else:
            availability = PrivacyVisibility(_availability)

        privacy_settings = cls(
            email=email,
            github=github,
            resume=resume,
            social_links=social_links,
            availability=availability,
        )

        privacy_settings.additional_properties = d
        return privacy_settings

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
