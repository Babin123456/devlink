from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.privacy_visibility import PrivacyVisibility
from ..types import UNSET, Unset

T = TypeVar("T", bound="PrivacySettingsUpdate")


@_attrs_define
class PrivacySettingsUpdate:
    """
    Attributes:
        email (None | PrivacyVisibility | Unset):
        github (None | PrivacyVisibility | Unset):
        resume (None | PrivacyVisibility | Unset):
        social_links (None | PrivacyVisibility | Unset):
        availability (None | PrivacyVisibility | Unset):
    """

    email: None | PrivacyVisibility | Unset = UNSET
    github: None | PrivacyVisibility | Unset = UNSET
    resume: None | PrivacyVisibility | Unset = UNSET
    social_links: None | PrivacyVisibility | Unset = UNSET
    availability: None | PrivacyVisibility | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        elif isinstance(self.email, PrivacyVisibility):
            email = self.email.value
        else:
            email = self.email

        github: None | str | Unset
        if isinstance(self.github, Unset):
            github = UNSET
        elif isinstance(self.github, PrivacyVisibility):
            github = self.github.value
        else:
            github = self.github

        resume: None | str | Unset
        if isinstance(self.resume, Unset):
            resume = UNSET
        elif isinstance(self.resume, PrivacyVisibility):
            resume = self.resume.value
        else:
            resume = self.resume

        social_links: None | str | Unset
        if isinstance(self.social_links, Unset):
            social_links = UNSET
        elif isinstance(self.social_links, PrivacyVisibility):
            social_links = self.social_links.value
        else:
            social_links = self.social_links

        availability: None | str | Unset
        if isinstance(self.availability, Unset):
            availability = UNSET
        elif isinstance(self.availability, PrivacyVisibility):
            availability = self.availability.value
        else:
            availability = self.availability

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

        def _parse_email(data: object) -> None | PrivacyVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                email_type_0 = PrivacyVisibility(data)

                return email_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PrivacyVisibility | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_github(data: object) -> None | PrivacyVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                github_type_0 = PrivacyVisibility(data)

                return github_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PrivacyVisibility | Unset, data)

        github = _parse_github(d.pop("github", UNSET))

        def _parse_resume(data: object) -> None | PrivacyVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resume_type_0 = PrivacyVisibility(data)

                return resume_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PrivacyVisibility | Unset, data)

        resume = _parse_resume(d.pop("resume", UNSET))

        def _parse_social_links(data: object) -> None | PrivacyVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                social_links_type_0 = PrivacyVisibility(data)

                return social_links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PrivacyVisibility | Unset, data)

        social_links = _parse_social_links(d.pop("social_links", UNSET))

        def _parse_availability(data: object) -> None | PrivacyVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                availability_type_0 = PrivacyVisibility(data)

                return availability_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PrivacyVisibility | Unset, data)

        availability = _parse_availability(d.pop("availability", UNSET))

        privacy_settings_update = cls(
            email=email,
            github=github,
            resume=resume,
            social_links=social_links,
            availability=availability,
        )

        privacy_settings_update.additional_properties = d
        return privacy_settings_update

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
