from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hackathon_team_member_response import HackathonTeamMemberResponse


T = TypeVar("T", bound="HackathonTeamResponse")


@_attrs_define
class HackathonTeamResponse:
    """
    Attributes:
        name (str):
        id (UUID):
        hackathon_id (UUID):
        created_by (UUID):
        member_count (int):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (None | str | Unset):
        members (list[HackathonTeamMemberResponse] | Unset):
    """

    name: str
    id: UUID
    hackathon_id: UUID
    created_by: UUID
    member_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: None | str | Unset = UNSET
    members: list[HackathonTeamMemberResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id = str(self.id)

        hackathon_id = str(self.hackathon_id)

        created_by = str(self.created_by)

        member_count = self.member_count

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        members: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.members, Unset):
            members = []
            for members_item_data in self.members:
                members_item = members_item_data.to_dict()
                members.append(members_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "hackathon_id": hackathon_id,
                "created_by": created_by,
                "member_count": member_count,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if members is not UNSET:
            field_dict["members"] = members

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hackathon_team_member_response import HackathonTeamMemberResponse

        d = dict(src_dict)
        name = d.pop("name")

        id = UUID(d.pop("id"))

        hackathon_id = UUID(d.pop("hackathon_id"))

        created_by = UUID(d.pop("created_by"))

        member_count = d.pop("member_count")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _members = d.pop("members", UNSET)
        members: list[HackathonTeamMemberResponse] | Unset = UNSET
        if _members is not UNSET:
            members = []
            for members_item_data in _members:
                members_item = HackathonTeamMemberResponse.from_dict(members_item_data)

                members.append(members_item)

        hackathon_team_response = cls(
            name=name,
            id=id,
            hackathon_id=hackathon_id,
            created_by=created_by,
            member_count=member_count,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            members=members,
        )

        hackathon_team_response.additional_properties = d
        return hackathon_team_response

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
