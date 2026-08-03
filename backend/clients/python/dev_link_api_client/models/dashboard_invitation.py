from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.member_role import MemberRole

T = TypeVar("T", bound="DashboardInvitation")


@_attrs_define
class DashboardInvitation:
    """
    Attributes:
        user_id (UUID):
        username (str):
        full_name (None | str):
        profile_image (None | str):
        role (MemberRole):
        invited_at (datetime.datetime):
    """

    user_id: UUID
    username: str
    full_name: None | str
    profile_image: None | str
    role: MemberRole
    invited_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = str(self.user_id)

        username = self.username

        full_name: None | str
        full_name = self.full_name

        profile_image: None | str
        profile_image = self.profile_image

        role = self.role.value

        invited_at = self.invited_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "profile_image": profile_image,
                "role": role,
                "invited_at": invited_at,
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

        invited_at = datetime.datetime.fromisoformat(d.pop("invited_at"))

        dashboard_invitation = cls(
            user_id=user_id,
            username=username,
            full_name=full_name,
            profile_image=profile_image,
            role=role,
            invited_at=invited_at,
        )

        dashboard_invitation.additional_properties = d
        return dashboard_invitation

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
