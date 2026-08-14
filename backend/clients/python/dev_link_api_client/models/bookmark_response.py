from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bookmark_target_type import BookmarkTargetType

T = TypeVar("T", bound="BookmarkResponse")


@_attrs_define
class BookmarkResponse:
    """
    Attributes:
        id (UUID):
        user_id (UUID):
        target_type (BookmarkTargetType):
        target_id (UUID):
        created_at (datetime.datetime):
    """

    id: UUID
    user_id: UUID
    target_type: BookmarkTargetType
    target_id: UUID
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = str(self.user_id)

        target_type = self.target_type.value

        target_id = str(self.target_id)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "target_type": target_type,
                "target_id": target_id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        user_id = UUID(d.pop("user_id"))

        target_type = BookmarkTargetType(d.pop("target_type"))

        target_id = UUID(d.pop("target_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        bookmark_response = cls(
            id=id,
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            created_at=created_at,
        )

        bookmark_response.additional_properties = d
        return bookmark_response

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
