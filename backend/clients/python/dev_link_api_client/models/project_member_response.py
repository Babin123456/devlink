from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.member_role import MemberRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectMemberResponse")


@_attrs_define
class ProjectMemberResponse:
    """
    Attributes:
        id (str | UUID):
        project_id (str | UUID):
        user_id (str | UUID):
        role (MemberRole):
        is_active (bool):
        joined_at (datetime.datetime):
        username (None | str | Unset):
        first_name (None | str | Unset):
        last_name (None | str | Unset):
        avatar_url (None | str | Unset):
    """

    id: str | UUID
    project_id: str | UUID
    user_id: str | UUID
    role: MemberRole
    is_active: bool
    joined_at: datetime.datetime
    username: None | str | Unset = UNSET
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET
    avatar_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: str
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        project_id: str
        if isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        user_id: str
        if isinstance(self.user_id, UUID):
            user_id = str(self.user_id)
        else:
            user_id = self.user_id

        role = self.role.value

        is_active = self.is_active

        joined_at = self.joined_at.isoformat()

        username: None | str | Unset
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        avatar_url: None | str | Unset
        if isinstance(self.avatar_url, Unset):
            avatar_url = UNSET
        else:
            avatar_url = self.avatar_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "user_id": user_id,
                "role": role,
                "is_active": is_active,
                "joined_at": joined_at,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_id(data: object) -> str | UUID:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | UUID, data)

        id = _parse_id(d.pop("id"))

        def _parse_project_id(data: object) -> str | UUID:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | UUID, data)

        project_id = _parse_project_id(d.pop("project_id"))

        def _parse_user_id(data: object) -> str | UUID:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_id_type_0 = UUID(data)

                return user_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | UUID, data)

        user_id = _parse_user_id(d.pop("user_id"))

        role = MemberRole(d.pop("role"))

        is_active = d.pop("is_active")

        joined_at = datetime.datetime.fromisoformat(d.pop("joined_at"))

        def _parse_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        def _parse_avatar_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        avatar_url = _parse_avatar_url(d.pop("avatar_url", UNSET))

        project_member_response = cls(
            id=id,
            project_id=project_id,
            user_id=user_id,
            role=role,
            is_active=is_active,
            joined_at=joined_at,
            username=username,
            first_name=first_name,
            last_name=last_name,
            avatar_url=avatar_url,
        )

        project_member_response.additional_properties = d
        return project_member_response

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
