from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProfileViewResponse")


@_attrs_define
class ProfileViewResponse:
    """
    Attributes:
        id (UUID):
        viewer_name (str):
        viewer_username (str):
        viewed_at (datetime.datetime):
        is_anonymous (bool):
        viewer_id (None | Unset | UUID):
        viewer_avatar (None | str | Unset):
    """

    id: UUID
    viewer_name: str
    viewer_username: str
    viewed_at: datetime.datetime
    is_anonymous: bool
    viewer_id: None | Unset | UUID = UNSET
    viewer_avatar: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        viewer_name = self.viewer_name

        viewer_username = self.viewer_username

        viewed_at = self.viewed_at.isoformat()

        is_anonymous = self.is_anonymous

        viewer_id: None | str | Unset
        if isinstance(self.viewer_id, Unset):
            viewer_id = UNSET
        elif isinstance(self.viewer_id, UUID):
            viewer_id = str(self.viewer_id)
        else:
            viewer_id = self.viewer_id

        viewer_avatar: None | str | Unset
        if isinstance(self.viewer_avatar, Unset):
            viewer_avatar = UNSET
        else:
            viewer_avatar = self.viewer_avatar

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "viewer_name": viewer_name,
                "viewer_username": viewer_username,
                "viewed_at": viewed_at,
                "is_anonymous": is_anonymous,
            }
        )
        if viewer_id is not UNSET:
            field_dict["viewer_id"] = viewer_id
        if viewer_avatar is not UNSET:
            field_dict["viewer_avatar"] = viewer_avatar

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        viewer_name = d.pop("viewer_name")

        viewer_username = d.pop("viewer_username")

        viewed_at = datetime.datetime.fromisoformat(d.pop("viewed_at"))

        is_anonymous = d.pop("is_anonymous")

        def _parse_viewer_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                viewer_id_type_0 = UUID(data)

                return viewer_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        viewer_id = _parse_viewer_id(d.pop("viewer_id", UNSET))

        def _parse_viewer_avatar(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        viewer_avatar = _parse_viewer_avatar(d.pop("viewer_avatar", UNSET))

        profile_view_response = cls(
            id=id,
            viewer_name=viewer_name,
            viewer_username=viewer_username,
            viewed_at=viewed_at,
            is_anonymous=is_anonymous,
            viewer_id=viewer_id,
            viewer_avatar=viewer_avatar,
        )

        profile_view_response.additional_properties = d
        return profile_view_response

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
