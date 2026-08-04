from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.message_type import MessageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageCreate")


@_attrs_define
class MessageCreate:
    """
    Attributes:
        content (str):
        conversation_id (UUID):
        type_ (MessageType | Unset):
        parent_message_id (None | Unset | UUID):
        attachment_url (None | str | Unset):
        attachment_name (None | str | Unset):
        attachment_size (int | None | Unset):
        mime_type (None | str | Unset):
    """

    content: str
    conversation_id: UUID
    type_: MessageType | Unset = UNSET
    parent_message_id: None | Unset | UUID = UNSET
    attachment_url: None | str | Unset = UNSET
    attachment_name: None | str | Unset = UNSET
    attachment_size: int | None | Unset = UNSET
    mime_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        conversation_id = str(self.conversation_id)

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        parent_message_id: None | str | Unset
        if isinstance(self.parent_message_id, Unset):
            parent_message_id = UNSET
        elif isinstance(self.parent_message_id, UUID):
            parent_message_id = str(self.parent_message_id)
        else:
            parent_message_id = self.parent_message_id

        attachment_url: None | str | Unset
        if isinstance(self.attachment_url, Unset):
            attachment_url = UNSET
        else:
            attachment_url = self.attachment_url

        attachment_name: None | str | Unset
        if isinstance(self.attachment_name, Unset):
            attachment_name = UNSET
        else:
            attachment_name = self.attachment_name

        attachment_size: int | None | Unset
        if isinstance(self.attachment_size, Unset):
            attachment_size = UNSET
        else:
            attachment_size = self.attachment_size

        mime_type: None | str | Unset
        if isinstance(self.mime_type, Unset):
            mime_type = UNSET
        else:
            mime_type = self.mime_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "conversation_id": conversation_id,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if parent_message_id is not UNSET:
            field_dict["parent_message_id"] = parent_message_id
        if attachment_url is not UNSET:
            field_dict["attachment_url"] = attachment_url
        if attachment_name is not UNSET:
            field_dict["attachment_name"] = attachment_name
        if attachment_size is not UNSET:
            field_dict["attachment_size"] = attachment_size
        if mime_type is not UNSET:
            field_dict["mime_type"] = mime_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        conversation_id = UUID(d.pop("conversation_id"))

        _type_ = d.pop("type", UNSET)
        type_: MessageType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = MessageType(_type_)

        def _parse_parent_message_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_message_id_type_0 = UUID(data)

                return parent_message_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        parent_message_id = _parse_parent_message_id(d.pop("parent_message_id", UNSET))

        def _parse_attachment_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        attachment_url = _parse_attachment_url(d.pop("attachment_url", UNSET))

        def _parse_attachment_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        attachment_name = _parse_attachment_name(d.pop("attachment_name", UNSET))

        def _parse_attachment_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        attachment_size = _parse_attachment_size(d.pop("attachment_size", UNSET))

        def _parse_mime_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        mime_type = _parse_mime_type(d.pop("mime_type", UNSET))

        message_create = cls(
            content=content,
            conversation_id=conversation_id,
            type_=type_,
            parent_message_id=parent_message_id,
            attachment_url=attachment_url,
            attachment_name=attachment_name,
            attachment_size=attachment_size,
            mime_type=mime_type,
        )

        message_create.additional_properties = d
        return message_create

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
