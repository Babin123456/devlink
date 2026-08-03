from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BookmarkCollectionResponse")


@_attrs_define
class BookmarkCollectionResponse:
    """
    Attributes:
        id (UUID):
        user_id (UUID):
        name (str):
        is_default (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        bookmark_count (int | Unset):  Default: 0.
    """

    id: UUID
    user_id: UUID
    name: str
    is_default: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    bookmark_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = str(self.user_id)

        name = self.name

        is_default = self.is_default

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        bookmark_count = self.bookmark_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "name": name,
                "is_default": is_default,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if bookmark_count is not UNSET:
            field_dict["bookmark_count"] = bookmark_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        user_id = UUID(d.pop("user_id"))

        name = d.pop("name")

        is_default = d.pop("is_default")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        bookmark_count = d.pop("bookmark_count", UNSET)

        bookmark_collection_response = cls(
            id=id,
            user_id=user_id,
            name=name,
            is_default=is_default,
            created_at=created_at,
            updated_at=updated_at,
            bookmark_count=bookmark_count,
        )

        bookmark_collection_response.additional_properties = d
        return bookmark_collection_response

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
