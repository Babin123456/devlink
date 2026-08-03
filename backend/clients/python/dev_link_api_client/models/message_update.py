from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageUpdate")


@_attrs_define
class MessageUpdate:
    """
    Attributes:
        content (None | str | Unset):
        is_edited (bool | None | Unset):
        is_deleted (bool | None | Unset):
    """

    content: None | str | Unset = UNSET
    is_edited: bool | None | Unset = UNSET
    is_deleted: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content: None | str | Unset
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        is_edited: bool | None | Unset
        if isinstance(self.is_edited, Unset):
            is_edited = UNSET
        else:
            is_edited = self.is_edited

        is_deleted: bool | None | Unset
        if isinstance(self.is_deleted, Unset):
            is_deleted = UNSET
        else:
            is_deleted = self.is_deleted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if is_edited is not UNSET:
            field_dict["is_edited"] = is_edited
        if is_deleted is not UNSET:
            field_dict["is_deleted"] = is_deleted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_content(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_is_edited(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_edited = _parse_is_edited(d.pop("is_edited", UNSET))

        def _parse_is_deleted(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        is_deleted = _parse_is_deleted(d.pop("is_deleted", UNSET))

        message_update = cls(
            content=content,
            is_edited=is_edited,
            is_deleted=is_deleted,
        )

        message_update.additional_properties = d
        return message_update

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
