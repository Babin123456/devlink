from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flare_status import FlareStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="BuilderFlareResponse")


@_attrs_define
class BuilderFlareResponse:
    """
    Attributes:
        title (str):
        description (str):
        role (str):
        id (UUID):
        project_id (UUID):
        created_by (UUID):
        applicants_count (int):
        featured (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        location (None | str | Unset):
        commitment (None | str | Unset):
        experience_level (None | str | Unset):
        openings (int | Unset):  Default: 1.
        status (FlareStatus | Unset):
        remote (bool | Unset):  Default: True.
    """

    title: str
    description: str
    role: str
    id: UUID
    project_id: UUID
    created_by: UUID
    applicants_count: int
    featured: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    location: None | str | Unset = UNSET
    commitment: None | str | Unset = UNSET
    experience_level: None | str | Unset = UNSET
    openings: int | Unset = 1
    status: FlareStatus | Unset = UNSET
    remote: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        role = self.role

        id = str(self.id)

        project_id = str(self.project_id)

        created_by = str(self.created_by)

        applicants_count = self.applicants_count

        featured = self.featured

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        location: None | str | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        else:
            location = self.location

        commitment: None | str | Unset
        if isinstance(self.commitment, Unset):
            commitment = UNSET
        else:
            commitment = self.commitment

        experience_level: None | str | Unset
        if isinstance(self.experience_level, Unset):
            experience_level = UNSET
        else:
            experience_level = self.experience_level

        openings = self.openings

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        remote = self.remote

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "description": description,
                "role": role,
                "id": id,
                "project_id": project_id,
                "created_by": created_by,
                "applicants_count": applicants_count,
                "featured": featured,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if location is not UNSET:
            field_dict["location"] = location
        if commitment is not UNSET:
            field_dict["commitment"] = commitment
        if experience_level is not UNSET:
            field_dict["experience_level"] = experience_level
        if openings is not UNSET:
            field_dict["openings"] = openings
        if status is not UNSET:
            field_dict["status"] = status
        if remote is not UNSET:
            field_dict["remote"] = remote

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        description = d.pop("description")

        role = d.pop("role")

        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        created_by = UUID(d.pop("created_by"))

        applicants_count = d.pop("applicants_count")

        featured = d.pop("featured")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_location(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_commitment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        commitment = _parse_commitment(d.pop("commitment", UNSET))

        def _parse_experience_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience_level = _parse_experience_level(d.pop("experience_level", UNSET))

        openings = d.pop("openings", UNSET)

        _status = d.pop("status", UNSET)
        status: FlareStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = FlareStatus(_status)

        remote = d.pop("remote", UNSET)

        builder_flare_response = cls(
            title=title,
            description=description,
            role=role,
            id=id,
            project_id=project_id,
            created_by=created_by,
            applicants_count=applicants_count,
            featured=featured,
            created_at=created_at,
            updated_at=updated_at,
            location=location,
            commitment=commitment,
            experience_level=experience_level,
            openings=openings,
            status=status,
            remote=remote,
        )

        builder_flare_response.additional_properties = d
        return builder_flare_response

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
