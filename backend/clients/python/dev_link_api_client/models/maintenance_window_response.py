from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceWindowResponse")


@_attrs_define
class MaintenanceWindowResponse:
    """
    Attributes:
        start_time (datetime.datetime): Start time of maintenance
        end_time (datetime.datetime): End time of maintenance
        id (UUID):
        created_at (datetime.datetime):
        message (str | Unset): Message to display to users Default: 'The system is undergoing scheduled maintenance.'.
        is_active (bool | Unset): Whether the window is active Default: True.
        created_by (None | Unset | UUID):
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    id: UUID
    created_at: datetime.datetime
    message: str | Unset = "The system is undergoing scheduled maintenance."
    is_active: bool | Unset = True
    created_by: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        id = str(self.id)

        created_at = self.created_at.isoformat()

        message = self.message

        is_active = self.is_active

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        elif isinstance(self.created_by, UUID):
            created_by = str(self.created_by)
        else:
            created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
                "end_time": end_time,
                "id": id,
                "created_at": created_at,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))

        end_time = datetime.datetime.fromisoformat(d.pop("end_time"))

        id = UUID(d.pop("id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        message = d.pop("message", UNSET)

        is_active = d.pop("is_active", UNSET)

        def _parse_created_by(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_type_0 = UUID(data)

                return created_by_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        maintenance_window_response = cls(
            start_time=start_time,
            end_time=end_time,
            id=id,
            created_at=created_at,
            message=message,
            is_active=is_active,
            created_by=created_by,
        )

        maintenance_window_response.additional_properties = d
        return maintenance_window_response

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
