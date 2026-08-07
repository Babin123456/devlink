from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CurrentUserResponse")


@_attrs_define
class CurrentUserResponse:
    """
    Attributes:
        id (UUID):
        first_name (str):
        last_name (str):
        username (str):
        email (str):
        is_verified (bool):
        is_active (bool):
        created_at (datetime.datetime):
        profile_image (None | str | Unset):
        last_seen (datetime.datetime | None | Unset): The date and time when the user was last active.
        is_online (bool | Unset): Whether the user is currently online based on the active threshold. Default: False.
        last_active_at (datetime.datetime | None | Unset):
    """

    id: UUID
    first_name: str
    last_name: str
    username: str
    email: str
    is_verified: bool
    is_active: bool
    created_at: datetime.datetime
    profile_image: None | str | Unset = UNSET
    last_seen: datetime.datetime | None | Unset = UNSET
    is_online: bool | Unset = False
    last_active_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        first_name = self.first_name

        last_name = self.last_name

        username = self.username

        email = self.email

        is_verified = self.is_verified

        is_active = self.is_active

        created_at = self.created_at.isoformat()

        profile_image: None | str | Unset
        if isinstance(self.profile_image, Unset):
            profile_image = UNSET
        else:
            profile_image = self.profile_image

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
                "is_verified": is_verified,
                "is_active": is_active,
                "created_at": created_at,
            }
        )
        if profile_image is not UNSET:
            field_dict["profile_image"] = profile_image
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if is_online is not UNSET:
            field_dict["is_online"] = is_online
        if last_active_at is not UNSET:
            field_dict["last_active_at"] = last_active_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        username = d.pop("username")

        email = d.pop("email")

        is_verified = d.pop("is_verified")

        is_active = d.pop("is_active")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_profile_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile_image = _parse_profile_image(d.pop("profile_image", UNSET))

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

        current_user_response = cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            is_verified=is_verified,
            is_active=is_active,
            created_at=created_at,
            profile_image=profile_image,
            last_seen=last_seen,
            is_online=is_online,
            last_active_at=last_active_at,
        )

        current_user_response.additional_properties = d
        return current_user_response

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
