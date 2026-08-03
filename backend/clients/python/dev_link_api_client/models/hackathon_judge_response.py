from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HackathonJudgeResponse")


@_attrs_define
class HackathonJudgeResponse:
    """
    Attributes:
        id (UUID):
        hackathon_id (UUID):
        user_id (UUID):
        created_at (datetime.datetime):
    """

    id: UUID
    hackathon_id: UUID
    user_id: UUID
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        hackathon_id = str(self.hackathon_id)

        user_id = str(self.user_id)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "hackathon_id": hackathon_id,
                "user_id": user_id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        hackathon_id = UUID(d.pop("hackathon_id"))

        user_id = UUID(d.pop("user_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        hackathon_judge_response = cls(
            id=id,
            hackathon_id=hackathon_id,
            user_id=user_id,
            created_at=created_at,
        )

        hackathon_judge_response.additional_properties = d
        return hackathon_judge_response

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
