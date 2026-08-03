from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bookmark_response import BookmarkResponse


T = TypeVar("T", bound="BookmarkCollectionWithBookmarks")


@_attrs_define
class BookmarkCollectionWithBookmarks:
    """
    Attributes:
        id (UUID):
        user_id (UUID):
        name (str):
        is_default (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        bookmarks (list[BookmarkResponse] | Unset):
    """

    id: UUID
    user_id: UUID
    name: str
    is_default: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    bookmarks: list[BookmarkResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = str(self.user_id)

        name = self.name

        is_default = self.is_default

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        bookmarks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.bookmarks, Unset):
            bookmarks = []
            for bookmarks_item_data in self.bookmarks:
                bookmarks_item = bookmarks_item_data.to_dict()
                bookmarks.append(bookmarks_item)

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
        if bookmarks is not UNSET:
            field_dict["bookmarks"] = bookmarks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bookmark_response import BookmarkResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        user_id = UUID(d.pop("user_id"))

        name = d.pop("name")

        is_default = d.pop("is_default")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        _bookmarks = d.pop("bookmarks", UNSET)
        bookmarks: list[BookmarkResponse] | Unset = UNSET
        if _bookmarks is not UNSET:
            bookmarks = []
            for bookmarks_item_data in _bookmarks:
                bookmarks_item = BookmarkResponse.from_dict(bookmarks_item_data)

                bookmarks.append(bookmarks_item)

        bookmark_collection_with_bookmarks = cls(
            id=id,
            user_id=user_id,
            name=name,
            is_default=is_default,
            created_at=created_at,
            updated_at=updated_at,
            bookmarks=bookmarks,
        )

        bookmark_collection_with_bookmarks.additional_properties = d
        return bookmark_collection_with_bookmarks

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
