from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.conversation_type import ConversationType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConversationResponse")


@_attrs_define
class ConversationResponse:
    """
    Attributes:
        id (UUID):
        created_by (UUID):
        is_active (bool):
        archived (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        type_ (ConversationType | Unset):
        title (None | str | Unset):
        project_id (None | Unset | UUID):
    """

    id: UUID
    created_by: UUID
    is_active: bool
    archived: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    type_: ConversationType | Unset = UNSET
    title: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        created_by = str(self.created_by)

        is_active = self.is_active

        archived = self.archived

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_by": created_by,
                "is_active": is_active,
                "archived": archived,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if title is not UNSET:
            field_dict["title"] = title
        if project_id is not UNSET:
            field_dict["project_id"] = project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        created_by = UUID(d.pop("created_by"))

        is_active = d.pop("is_active")

        archived = d.pop("archived")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        _type_ = d.pop("type", UNSET)
        type_: ConversationType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ConversationType(_type_)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_id_type_0 = UUID(data)

                return project_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        conversation_response = cls(
            id=id,
            created_by=created_by,
            is_active=is_active,
            archived=archived,
            created_at=created_at,
            updated_at=updated_at,
            type_=type_,
            title=title,
            project_id=project_id,
        )

        conversation_response.additional_properties = d
        return conversation_response

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
