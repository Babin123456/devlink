from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.submission_status import SubmissionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="HackathonSubmissionResponse")


@_attrs_define
class HackathonSubmissionResponse:
    """
    Attributes:
        title (str):
        description (str):
        id (UUID):
        hackathon_id (UUID):
        team_id (UUID):
        submitted_by (UUID):
        status (SubmissionStatus):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        repo_url (None | str | Unset):
        demo_url (None | str | Unset):
    """

    title: str
    description: str
    id: UUID
    hackathon_id: UUID
    team_id: UUID
    submitted_by: UUID
    status: SubmissionStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    repo_url: None | str | Unset = UNSET
    demo_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        id = str(self.id)

        hackathon_id = str(self.hackathon_id)

        team_id = str(self.team_id)

        submitted_by = str(self.submitted_by)

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        repo_url: None | str | Unset
        if isinstance(self.repo_url, Unset):
            repo_url = UNSET
        else:
            repo_url = self.repo_url

        demo_url: None | str | Unset
        if isinstance(self.demo_url, Unset):
            demo_url = UNSET
        else:
            demo_url = self.demo_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "description": description,
                "id": id,
                "hackathon_id": hackathon_id,
                "team_id": team_id,
                "submitted_by": submitted_by,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if repo_url is not UNSET:
            field_dict["repo_url"] = repo_url
        if demo_url is not UNSET:
            field_dict["demo_url"] = demo_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        description = d.pop("description")

        id = UUID(d.pop("id"))

        hackathon_id = UUID(d.pop("hackathon_id"))

        team_id = UUID(d.pop("team_id"))

        submitted_by = UUID(d.pop("submitted_by"))

        status = SubmissionStatus(d.pop("status"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_repo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        repo_url = _parse_repo_url(d.pop("repo_url", UNSET))

        def _parse_demo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        demo_url = _parse_demo_url(d.pop("demo_url", UNSET))

        hackathon_submission_response = cls(
            title=title,
            description=description,
            id=id,
            hackathon_id=hackathon_id,
            team_id=team_id,
            submitted_by=submitted_by,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            repo_url=repo_url,
            demo_url=demo_url,
        )

        hackathon_submission_response.additional_properties = d
        return hackathon_submission_response

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
