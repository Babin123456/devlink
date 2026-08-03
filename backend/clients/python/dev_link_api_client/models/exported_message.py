from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportedMessage")


@_attrs_define
class ExportedMessage:
    """
    Attributes:
        id (UUID):
        conversation_id (UUID):
        content (str):
        type_ (str):
        created_at (datetime.datetime):
    """

    id: UUID
    conversation_id: UUID
    content: str
    type_: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        conversation_id = str(self.conversation_id)

        content = self.content

        type_ = self.type_

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "conversation_id": conversation_id,
                "content": content,
                "type": type_,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        conversation_id = UUID(d.pop("conversation_id"))

        content = d.pop("content")

        type_ = d.pop("type")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        exported_message = cls(
            id=id,
            conversation_id=conversation_id,
            content=content,
            type_=type_,
            created_at=created_at,
        )

        exported_message.additional_properties = d
        return exported_message

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
