from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserReportResponse")


@_attrs_define
class UserReportResponse:
    """
    Attributes:
        reason (str):
        id (UUID):
        reporter_id (UUID):
        reported_id (UUID):
        status (str):
        created_at (datetime.datetime):
        description (None | str | Unset):
    """

    reason: str
    id: UUID
    reporter_id: UUID
    reported_id: UUID
    status: str
    created_at: datetime.datetime
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reason = self.reason

        id = str(self.id)

        reporter_id = str(self.reporter_id)

        reported_id = str(self.reported_id)

        status = self.status

        created_at = self.created_at.isoformat()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reason": reason,
                "id": id,
                "reporter_id": reporter_id,
                "reported_id": reported_id,
                "status": status,
                "created_at": created_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reason = d.pop("reason")

        id = UUID(d.pop("id"))

        reporter_id = UUID(d.pop("reporter_id"))

        reported_id = UUID(d.pop("reported_id"))

        status = d.pop("status")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        user_report_response = cls(
            reason=reason,
            id=id,
            reporter_id=reporter_id,
            reported_id=reported_id,
            status=status,
            created_at=created_at,
            description=description,
        )

        user_report_response.additional_properties = d
        return user_report_response

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
