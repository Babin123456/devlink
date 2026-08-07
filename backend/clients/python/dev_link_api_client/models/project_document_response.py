from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectDocumentResponse")


@_attrs_define
class ProjectDocumentResponse:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        version (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        title (str | Unset):  Default: 'Untitled Document'.
        content (str | Unset):  Default: ''.
        created_by_id (None | Unset | UUID):
        last_edited_by_id (None | Unset | UUID):
        conflict (bool | Unset):  Default: False.
    """

    id: UUID
    project_id: UUID
    version: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    title: str | Unset = "Untitled Document"
    content: str | Unset = ""
    created_by_id: None | Unset | UUID = UNSET
    last_edited_by_id: None | Unset | UUID = UNSET
    conflict: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        version = self.version

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        title = self.title

        content = self.content

        created_by_id: None | str | Unset
        if isinstance(self.created_by_id, Unset):
            created_by_id = UNSET
        elif isinstance(self.created_by_id, UUID):
            created_by_id = str(self.created_by_id)
        else:
            created_by_id = self.created_by_id

        last_edited_by_id: None | str | Unset
        if isinstance(self.last_edited_by_id, Unset):
            last_edited_by_id = UNSET
        elif isinstance(self.last_edited_by_id, UUID):
            last_edited_by_id = str(self.last_edited_by_id)
        else:
            last_edited_by_id = self.last_edited_by_id

        conflict = self.conflict

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "version": version,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if content is not UNSET:
            field_dict["content"] = content
        if created_by_id is not UNSET:
            field_dict["created_by_id"] = created_by_id
        if last_edited_by_id is not UNSET:
            field_dict["last_edited_by_id"] = last_edited_by_id
        if conflict is not UNSET:
            field_dict["conflict"] = conflict

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        version = d.pop("version")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        title = d.pop("title", UNSET)

        content = d.pop("content", UNSET)

        def _parse_created_by_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_id_type_0 = UUID(data)

                return created_by_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        created_by_id = _parse_created_by_id(d.pop("created_by_id", UNSET))

        def _parse_last_edited_by_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_edited_by_id_type_0 = UUID(data)

                return last_edited_by_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        last_edited_by_id = _parse_last_edited_by_id(d.pop("last_edited_by_id", UNSET))

        conflict = d.pop("conflict", UNSET)

        project_document_response = cls(
            id=id,
            project_id=project_id,
            version=version,
            created_at=created_at,
            updated_at=updated_at,
            title=title,
            content=content,
            created_by_id=created_by_id,
            last_edited_by_id=last_edited_by_id,
            conflict=conflict,
        )

        project_document_response.additional_properties = d
        return project_document_response

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
