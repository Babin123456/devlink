from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.message_type import MessageType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageResponse")


@_attrs_define
class MessageResponse:
    """
    Attributes:
        content (str):
        id (UUID):
        conversation_id (UUID):
        sender_id (UUID):
        is_edited (bool):
        is_deleted (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        type_ (MessageType | Unset):
        parent_message_id (None | Unset | UUID):
        attachment_url (None | str | Unset):
        attachment_name (None | str | Unset):
        attachment_size (int | None | Unset):
        mime_type (None | str | Unset):
        edited_at (datetime.datetime | None | Unset):
        deleted_at (datetime.datetime | None | Unset):
    """

    content: str
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    is_edited: bool
    is_deleted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    type_: MessageType | Unset = UNSET
    parent_message_id: None | Unset | UUID = UNSET
    attachment_url: None | str | Unset = UNSET
    attachment_name: None | str | Unset = UNSET
    attachment_size: int | None | Unset = UNSET
    mime_type: None | str | Unset = UNSET
    edited_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        id = str(self.id)

        conversation_id = str(self.conversation_id)

        sender_id = str(self.sender_id)

        is_edited = self.is_edited

        is_deleted = self.is_deleted

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        edited_at: None | str | Unset
        if isinstance(self.edited_at, Unset):
            edited_at = UNSET
        elif isinstance(self.edited_at, datetime.datetime):
            edited_at = self.edited_at.isoformat()
        else:
            edited_at = self.edited_at

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "id": id,
                "conversation_id": conversation_id,
                "sender_id": sender_id,
                "is_edited": is_edited,
                "is_deleted": is_deleted,
                "created_at": created_at,
                "updated_at": updated_at,
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
        if edited_at is not UNSET:
            field_dict["edited_at"] = edited_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        id = UUID(d.pop("id"))

        conversation_id = UUID(d.pop("conversation_id"))

        sender_id = UUID(d.pop("sender_id"))

        is_edited = d.pop("is_edited")

        is_deleted = d.pop("is_deleted")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

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

        def _parse_edited_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                edited_at_type_0 = datetime.datetime.fromisoformat(data)

                return edited_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        edited_at = _parse_edited_at(d.pop("edited_at", UNSET))

        def _parse_deleted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = datetime.datetime.fromisoformat(data)

                return deleted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        message_response = cls(
            content=content,
            id=id,
            conversation_id=conversation_id,
            sender_id=sender_id,
            is_edited=is_edited,
            is_deleted=is_deleted,
            created_at=created_at,
            updated_at=updated_at,
            type_=type_,
            parent_message_id=parent_message_id,
            attachment_url=attachment_url,
            attachment_name=attachment_name,
            attachment_size=attachment_size,
            mime_type=mime_type,
            edited_at=edited_at,
            deleted_at=deleted_at,
        )

        message_response.additional_properties = d
        return message_response

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
