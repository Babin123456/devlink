from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceWindowCreate")


@_attrs_define
class MaintenanceWindowCreate:
    """
    Attributes:
        start_time (datetime.datetime): Start time of maintenance
        end_time (datetime.datetime): End time of maintenance
        message (str | Unset): Message to display to users Default: 'The system is undergoing scheduled maintenance.'.
        is_active (bool | Unset): Whether the window is active Default: True.
    """

    start_time: datetime.datetime
    end_time: datetime.datetime
    message: str | Unset = "The system is undergoing scheduled maintenance."
    is_active: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time = self.start_time.isoformat()

        end_time = self.end_time.isoformat()

        message = self.message

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
                "end_time": end_time,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_time = datetime.datetime.fromisoformat(d.pop("start_time"))

        end_time = datetime.datetime.fromisoformat(d.pop("end_time"))

        message = d.pop("message", UNSET)

        is_active = d.pop("is_active", UNSET)

        maintenance_window_create = cls(
            start_time=start_time,
            end_time=end_time,
            message=message,
            is_active=is_active,
        )

        maintenance_window_create.additional_properties = d
        return maintenance_window_create

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
