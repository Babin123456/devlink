from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.registration_status import RegistrationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="HackathonRegistrationResponse")


@_attrs_define
class HackathonRegistrationResponse:
    """
    Attributes:
        id (UUID):
        hackathon_id (UUID):
        user_id (UUID):
        status (RegistrationStatus):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        motivation (None | str | Unset):
        experience_level (None | str | Unset):
        team_id (None | Unset | UUID):
    """

    id: UUID
    hackathon_id: UUID
    user_id: UUID
    status: RegistrationStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    motivation: None | str | Unset = UNSET
    experience_level: None | str | Unset = UNSET
    team_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        hackathon_id = str(self.hackathon_id)

        user_id = str(self.user_id)

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        motivation: None | str | Unset
        if isinstance(self.motivation, Unset):
            motivation = UNSET
        else:
            motivation = self.motivation

        experience_level: None | str | Unset
        if isinstance(self.experience_level, Unset):
            experience_level = UNSET
        else:
            experience_level = self.experience_level

        team_id: None | str | Unset
        if isinstance(self.team_id, Unset):
            team_id = UNSET
        elif isinstance(self.team_id, UUID):
            team_id = str(self.team_id)
        else:
            team_id = self.team_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "hackathon_id": hackathon_id,
                "user_id": user_id,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if motivation is not UNSET:
            field_dict["motivation"] = motivation
        if experience_level is not UNSET:
            field_dict["experience_level"] = experience_level
        if team_id is not UNSET:
            field_dict["team_id"] = team_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        hackathon_id = UUID(d.pop("hackathon_id"))

        user_id = UUID(d.pop("user_id"))

        status = RegistrationStatus(d.pop("status"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_motivation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        motivation = _parse_motivation(d.pop("motivation", UNSET))

        def _parse_experience_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience_level = _parse_experience_level(d.pop("experience_level", UNSET))

        def _parse_team_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                team_id_type_0 = UUID(data)

                return team_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        team_id = _parse_team_id(d.pop("team_id", UNSET))

        hackathon_registration_response = cls(
            id=id,
            hackathon_id=hackathon_id,
            user_id=user_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            motivation=motivation,
            experience_level=experience_level,
            team_id=team_id,
        )

        hackathon_registration_response.additional_properties = d
        return hackathon_registration_response

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
