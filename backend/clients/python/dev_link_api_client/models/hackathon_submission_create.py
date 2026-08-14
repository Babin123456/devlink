from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HackathonSubmissionCreate")


@_attrs_define
class HackathonSubmissionCreate:
    """
    Attributes:
        title (str):
        description (str):
        team_id (UUID):
        repo_url (None | str | Unset):
        demo_url (None | str | Unset):
    """

    title: str
    description: str
    team_id: UUID
    repo_url: None | str | Unset = UNSET
    demo_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        team_id = str(self.team_id)

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
                "team_id": team_id,
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

        team_id = UUID(d.pop("team_id"))

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

        hackathon_submission_create = cls(
            title=title,
            description=description,
            team_id=team_id,
            repo_url=repo_url,
            demo_url=demo_url,
        )

        hackathon_submission_create.additional_properties = d
        return hackathon_submission_create

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
