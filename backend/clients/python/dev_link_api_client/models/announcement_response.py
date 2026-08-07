from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.user_response import UserResponse


T = TypeVar("T", bound="AnnouncementResponse")


@_attrs_define
class AnnouncementResponse:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        author_id (UUID):
        title (str):
        content (str):
        created_at (datetime.datetime):
        author (UserResponse):
    """

    id: UUID
    project_id: UUID
    author_id: UUID
    title: str
    content: str
    created_at: datetime.datetime
    author: UserResponse
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        author_id = str(self.author_id)

        title = self.title

        content = self.content

        created_at = self.created_at.isoformat()

        author = self.author.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "author_id": author_id,
                "title": title,
                "content": content,
                "created_at": created_at,
                "author": author,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_response import UserResponse

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        author_id = UUID(d.pop("author_id"))

        title = d.pop("title")

        content = d.pop("content")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        author = UserResponse.from_dict(d.pop("author"))

        announcement_response = cls(
            id=id,
            project_id=project_id,
            author_id=author_id,
            title=title,
            content=content,
            created_at=created_at,
            author=author,
        )

        announcement_response.additional_properties = d
        return announcement_response

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
