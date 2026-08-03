from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MilestoneResponse")


@_attrs_define
class MilestoneResponse:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        title (str):
        description (None | str):
        due_date (datetime.datetime | None):
        is_completed (bool):
        created_at (datetime.datetime):
    """

    id: UUID
    project_id: UUID
    title: str
    description: None | str
    due_date: datetime.datetime | None
    is_completed: bool
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        title = self.title

        description: None | str
        description = self.description

        due_date: None | str
        if isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        is_completed = self.is_completed

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "title": title,
                "description": description,
                "due_date": due_date,
                "is_completed": is_completed,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        title = d.pop("title")

        def _parse_description(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        def _parse_due_date(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = datetime.datetime.fromisoformat(data)

                return due_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        due_date = _parse_due_date(d.pop("due_date"))

        is_completed = d.pop("is_completed")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        milestone_response = cls(
            id=id,
            project_id=project_id,
            title=title,
            description=description,
            due_date=due_date,
            is_completed=is_completed,
            created_at=created_at,
        )

        milestone_response.additional_properties = d
        return milestone_response

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
