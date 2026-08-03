from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ActivityActor")


@_attrs_define
class ActivityActor:
    """
    Attributes:
        id (UUID):
        first_name (str):
        last_name (str):
        username (str):
        profile_image (None | str | Unset):
    """

    id: UUID
    first_name: str
    last_name: str
    username: str
    profile_image: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        first_name = self.first_name

        last_name = self.last_name

        username = self.username

        profile_image: None | str | Unset
        if isinstance(self.profile_image, Unset):
            profile_image = UNSET
        else:
            profile_image = self.profile_image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
            }
        )
        if profile_image is not UNSET:
            field_dict["profile_image"] = profile_image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        first_name = d.pop("first_name")

        last_name = d.pop("last_name")

        username = d.pop("username")

        def _parse_profile_image(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        profile_image = _parse_profile_image(d.pop("profile_image", UNSET))

        activity_actor = cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            profile_image=profile_image,
        )

        activity_actor.additional_properties = d
        return activity_actor

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
