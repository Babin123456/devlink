from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.member_role import MemberRole

T = TypeVar("T", bound="DashboardMember")


@_attrs_define
class DashboardMember:
    """
    Attributes:
        user_id (UUID):
        username (str):
        full_name (None | str):
        profile_image (None | str):
        role (MemberRole):
        is_online (bool):
        last_seen (datetime.datetime | None):
    """

    user_id: UUID
    username: str
    full_name: None | str
    profile_image: None | str
    role: MemberRole
    is_online: bool
    last_seen: datetime.datetime | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = str(self.user_id)

        username = self.username

        full_name: None | str
        full_name = self.full_name

        profile_image: None | str
        profile_image = self.profile_image

        role = self.role.value

        is_online = self.is_online

        last_seen: None | str
        if isinstance(self.last_seen, datetime.datetime):
            last_seen = self.last_seen.isoformat()
        else:
            last_seen = self.last_seen

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "profile_image": profile_image,
                "role": role,
                "is_online": is_online,
                "last_seen": last_seen,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = UUID(d.pop("user_id"))

        username = d.pop("username")

        def _parse_full_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        full_name = _parse_full_name(d.pop("full_name"))

        def _parse_profile_image(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profile_image = _parse_profile_image(d.pop("profile_image"))

        role = MemberRole(d.pop("role"))

        is_online = d.pop("is_online")

        def _parse_last_seen(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_type_0 = datetime.datetime.fromisoformat(data)

                return last_seen_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_seen = _parse_last_seen(d.pop("last_seen"))

        dashboard_member = cls(
            user_id=user_id,
            username=username,
            full_name=full_name,
            profile_image=profile_image,
            role=role,
            is_online=is_online,
            last_seen=last_seen,
        )

        dashboard_member.additional_properties = d
        return dashboard_member

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
