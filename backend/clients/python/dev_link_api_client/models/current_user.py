from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.availability_slot import AvailabilitySlot
    from ..models.privacy_settings import PrivacySettings


T = TypeVar("T", bound="CurrentUser")


@_attrs_define
class CurrentUser:
    """
    Attributes:
        first_name (str):
        last_name (str):
        username (str):
        id (UUID):
        is_active (bool):
        is_verified (bool):
        is_superuser (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        email (str):
        public_email (None | str | Unset):
        headline (None | str | Unset):
        bio (None | str | Unset):
        location (None | str | Unset):
        timezone (None | str | Unset):
        website (None | str | Unset):
        resume_url (None | str | Unset):
        portfolio_url (None | str | Unset):
        github_url (None | str | Unset):
        linkedin_url (None | str | Unset):
        role (None | str | Unset):
        experience_level (None | str | Unset):
        company (None | str | Unset):
        open_to_work (bool | Unset):  Default: True.
        is_private (bool | Unset):  Default: False.
        privacy_settings (None | PrivacySettings | Unset):
        availability (list[AvailabilitySlot] | Unset):
        profile_image (None | str | Unset):
        cover_image (None | str | Unset):
        badges (list[str] | Unset):
        last_seen (datetime.datetime | None | Unset): The date and time when the user was last active.
        is_online (bool | Unset): Whether the user is currently online based on the active threshold. Default: False.
        last_active_at (datetime.datetime | None | Unset):
        deleted_at (datetime.datetime | None | Unset):
        deleted_by_id (None | Unset | UUID):
        email_verified_at (datetime.datetime | None | Unset):
        last_login (datetime.datetime | None | Unset):
    """

    first_name: str
    last_name: str
    username: str
    id: UUID
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    email: str
    public_email: None | str | Unset = UNSET
    headline: None | str | Unset = UNSET
    bio: None | str | Unset = UNSET
    location: None | str | Unset = UNSET
    timezone: None | str | Unset = UNSET
    website: None | str | Unset = UNSET
    resume_url: None | str | Unset = UNSET
    portfolio_url: None | str | Unset = UNSET
    github_url: None | str | Unset = UNSET
    linkedin_url: None | str | Unset = UNSET
    role: None | str | Unset = UNSET
    experience_level: None | str | Unset = UNSET
    company: None | str | Unset = UNSET
    open_to_work: bool | Unset = True
    is_private: bool | Unset = False
    privacy_settings: None | PrivacySettings | Unset = UNSET
    availability: list[AvailabilitySlot] | Unset = UNSET
    profile_image: None | str | Unset = UNSET
    cover_image: None | str | Unset = UNSET
    badges: list[str] | Unset = UNSET
    last_seen: datetime.datetime | None | Unset = UNSET
    is_online: bool | Unset = False
    last_active_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    deleted_by_id: None | Unset | UUID = UNSET
    email_verified_at: datetime.datetime | None | Unset = UNSET
    last_login: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.privacy_settings import PrivacySettings

        first_name = self.first_name

        last_name = self.last_name

        username = self.username

        id = str(self.id)

        is_active = self.is_active

        is_verified = self.is_verified

        is_superuser = self.is_superuser

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        email = self.email

        public_email: None | str | Unset
        if isinstance(self.public_email, Unset):
            public_email = UNSET
        else:
            public_email = self.public_email

        headline: None | str | Unset
        if isinstance(self.headline, Unset):
            headline = UNSET
        else:
            headline = self.headline

        bio: None | str | Unset
        if isinstance(self.bio, Unset):
            bio = UNSET
        else:
            bio = self.bio

        location: None | str | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        else:
            location = self.location

        timezone: None | str | Unset
        if isinstance(self.timezone, Unset):
            timezone = UNSET
        else:
            timezone = self.timezone

        website: None | str | Unset
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        resume_url: None | str | Unset
        if isinstance(self.resume_url, Unset):
            resume_url = UNSET
        else:
            resume_url = self.resume_url

        portfolio_url: None | str | Unset
        if isinstance(self.portfolio_url, Unset):
            portfolio_url = UNSET
        else:
            portfolio_url = self.portfolio_url

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

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        experience_level: None | str | Unset
        if isinstance(self.experience_level, Unset):
            experience_level = UNSET
        else:
            experience_level = self.experience_level

        company: None | str | Unset
        if isinstance(self.company, Unset):
            company = UNSET
        else:
            company = self.company

        open_to_work = self.open_to_work

        is_private = self.is_private

        privacy_settings: dict[str, Any] | None | Unset
        if isinstance(self.privacy_settings, Unset):
            privacy_settings = UNSET
        elif isinstance(self.privacy_settings, PrivacySettings):
            privacy_settings = self.privacy_settings.to_dict()
        else:
            privacy_settings = self.privacy_settings

        availability: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.availability, Unset):
            availability = []
            for availability_item_data in self.availability:
                availability_item = availability_item_data.to_dict()
                availability.append(availability_item)

        profile_image: None | str | Unset
        if isinstance(self.profile_image, Unset):
            profile_image = UNSET
        else:
            profile_image = self.profile_image

        cover_image: None | str | Unset
        if isinstance(self.cover_image, Unset):
            cover_image = UNSET
        else:
            cover_image = self.cover_image

        badges: list[str] | Unset = UNSET
        if not isinstance(self.badges, Unset):
            badges = self.badges

        last_seen: None | str | Unset
        if isinstance(self.last_seen, Unset):
            last_seen = UNSET
        elif isinstance(self.last_seen, datetime.datetime):
            last_seen = self.last_seen.isoformat()
        else:
            last_seen = self.last_seen

        is_online = self.is_online

        last_active_at: None | str | Unset
        if isinstance(self.last_active_at, Unset):
            last_active_at = UNSET
        elif isinstance(self.last_active_at, datetime.datetime):
            last_active_at = self.last_active_at.isoformat()
        else:
            last_active_at = self.last_active_at

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        deleted_by_id: None | str | Unset
        if isinstance(self.deleted_by_id, Unset):
            deleted_by_id = UNSET
        elif isinstance(self.deleted_by_id, UUID):
            deleted_by_id = str(self.deleted_by_id)
        else:
            deleted_by_id = self.deleted_by_id

        email_verified_at: None | str | Unset
        if isinstance(self.email_verified_at, Unset):
            email_verified_at = UNSET
        elif isinstance(self.email_verified_at, datetime.datetime):
            email_verified_at = self.email_verified_at.isoformat()
        else:
            email_verified_at = self.email_verified_at

        last_login: None | str | Unset
        if isinstance(self.last_login, Unset):
            last_login = UNSET
        elif isinstance(self.last_login, datetime.datetime):
            last_login = self.last_login.isoformat()
        else:
            last_login = self.last_login

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "id": id,
                "is_active": is_active,
                "is_verified": is_verified,
                "is_superuser": is_superuser,
                "created_at": created_at,
                "updated_at": updated_at,
                "email": email,
            }
        )
        if public_email is not UNSET:
            field_dict["public_email"] = public_email
        if headline is not UNSET:
            field_dict["headline"] = headline
        if bio is not UNSET:
            field_dict["bio"] = bio
        if location is not UNSET:
            field_dict["location"] = location
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if website is not UNSET:
            field_dict["website"] = website
        if resume_url is not UNSET:
            field_dict["resume_url"] = resume_url
        if portfolio_url is not UNSET:
            field_dict["portfolio_url"] = portfolio_url
        if github_url is not UNSET:
            field_dict["github_url"] = github_url
        if linkedin_url is not UNSET:
            field_dict["linkedin_url"] = linkedin_url
        if role is not UNSET:
            field_dict["role"] = role
        if experience_level is not UNSET:
            field_dict["experience_level"] = experience_level
        if company is not UNSET:
            field_dict["company"] = company
        if open_to_work is not UNSET:
            field_dict["open_to_work"] = open_to_work
        if is_private is not UNSET:
            field_dict["is_private"] = is_private
        if privacy_settings is not UNSET:
            field_dict["privacy_settings"] = privacy_settings
        if availability is not UNSET:
            field_dict["availability"] = availability
        if profile_image is not UNSET:
            field_dict["profile_image"] = profile_image
        if cover_image is not UNSET:
            field_dict["cover_image"] = cover_image
        if badges is not UNSET:
            field_dict["badges"] = badges
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if is_online is not UNSET:
            field_dict["is_online"] = is_online
        if last_active_at is not UNSET:
            field_dict["last_active_at"] = last_active_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if deleted_by_id is not UNSET:
            field_dict["deleted_by_id"] = deleted_by_id
        if email_verified_at is not UNSET:
            field_dict["email_verified_at"] = email_verified_at
        if last_login is not UNSET:
            field_dict["last_login"] = last_login

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.availability_slot import AvailabilitySlot
        from ..models.privacy_settings import PrivacySettings

        d = dict(src_dict)
        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        username = d.pop("username")

        id = UUID(d.pop("id"))

        is_active = d.pop("is_active")

        is_verified = d.pop("is_verified")

        is_superuser = d.pop("is_superuser")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        email = d.pop("email")

        def _parse_public_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        public_email = _parse_public_email(d.pop("public_email", UNSET))

        def _parse_headline(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        headline = _parse_headline(d.pop("headline", UNSET))

        def _parse_bio(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        bio = _parse_bio(d.pop("bio", UNSET))

        def _parse_location(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_timezone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        timezone = _parse_timezone(d.pop("timezone", UNSET))

        def _parse_website(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        website = _parse_website(d.pop("website", UNSET))

        def _parse_resume_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        resume_url = _parse_resume_url(d.pop("resume_url", UNSET))

        def _parse_portfolio_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        portfolio_url = _parse_portfolio_url(d.pop("portfolio_url", UNSET))

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

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_experience_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience_level = _parse_experience_level(d.pop("experience_level", UNSET))

        def _parse_company(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        company = _parse_company(d.pop("company", UNSET))

        open_to_work = d.pop("open_to_work", UNSET)

        is_private = d.pop("is_private", UNSET)

        def _parse_privacy_settings(data: object) -> None | PrivacySettings | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                privacy_settings_type_0 = PrivacySettings.from_dict(data)

                return privacy_settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PrivacySettings | Unset, data)

        privacy_settings = _parse_privacy_settings(d.pop("privacy_settings", UNSET))

        _availability = d.pop("availability", UNSET)
        availability: list[AvailabilitySlot] | Unset = UNSET
        if _availability is not UNSET:
            availability = []
            for availability_item_data in _availability:
                availability_item = AvailabilitySlot.from_dict(availability_item_data)

                availability.append(availability_item)

        def _parse_profile_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile_image = _parse_profile_image(d.pop("profile_image", UNSET))

        def _parse_cover_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cover_image = _parse_cover_image(d.pop("cover_image", UNSET))

        badges = cast(list[str], d.pop("badges", UNSET))

        def _parse_last_seen(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_type_0 = datetime.datetime.fromisoformat(data)

                return last_seen_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_seen = _parse_last_seen(d.pop("last_seen", UNSET))

        is_online = d.pop("is_online", UNSET)

        def _parse_last_active_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_active_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_active_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_active_at = _parse_last_active_at(d.pop("last_active_at", UNSET))

        def _parse_deleted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = datetime.datetime.fromisoformat(data)

                return deleted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_deleted_by_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_by_id_type_0 = UUID(data)

                return deleted_by_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        deleted_by_id = _parse_deleted_by_id(d.pop("deleted_by_id", UNSET))

        def _parse_email_verified_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                email_verified_at_type_0 = datetime.datetime.fromisoformat(data)

                return email_verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        email_verified_at = _parse_email_verified_at(d.pop("email_verified_at", UNSET))

        def _parse_last_login(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_login_type_0 = datetime.datetime.fromisoformat(data)

                return last_login_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_login = _parse_last_login(d.pop("last_login", UNSET))

        current_user = cls(
            first_name=first_name,
            last_name=last_name,
            username=username,
            id=id,
            is_active=is_active,
            is_verified=is_verified,
            is_superuser=is_superuser,
            created_at=created_at,
            updated_at=updated_at,
            email=email,
            public_email=public_email,
            headline=headline,
            bio=bio,
            location=location,
            timezone=timezone,
            website=website,
            resume_url=resume_url,
            portfolio_url=portfolio_url,
            github_url=github_url,
            linkedin_url=linkedin_url,
            role=role,
            experience_level=experience_level,
            company=company,
            open_to_work=open_to_work,
            is_private=is_private,
            privacy_settings=privacy_settings,
            availability=availability,
            profile_image=profile_image,
            cover_image=cover_image,
            badges=badges,
            last_seen=last_seen,
            is_online=is_online,
            last_active_at=last_active_at,
            deleted_at=deleted_at,
            deleted_by_id=deleted_by_id,
            email_verified_at=email_verified_at,
            last_login=last_login,
        )

        current_user.additional_properties = d
        return current_user

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
