from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportedProject")


@_attrs_define
class ExportedProject:
    """
    Attributes:
        id (UUID):
        title (str):
        slug (str):
        description (str):
        stage (str):
        visibility (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        tagline (None | str | Unset):
        tech_stack (None | str | Unset):
        repository_url (None | str | Unset):
        website_url (None | str | Unset):
        team_size (int | Unset):  Default: 1.
        hiring (bool | Unset):  Default: True.
        is_archived (bool | Unset):  Default: False.
    """

    id: UUID
    title: str
    slug: str
    description: str
    stage: str
    visibility: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tagline: None | str | Unset = UNSET
    tech_stack: None | str | Unset = UNSET
    repository_url: None | str | Unset = UNSET
    website_url: None | str | Unset = UNSET
    team_size: int | Unset = 1
    hiring: bool | Unset = True
    is_archived: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        title = self.title

        slug = self.slug

        description = self.description

        stage = self.stage

        visibility = self.visibility

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        tagline: None | str | Unset
        if isinstance(self.tagline, Unset):
            tagline = UNSET
        else:
            tagline = self.tagline

        tech_stack: None | str | Unset
        if isinstance(self.tech_stack, Unset):
            tech_stack = UNSET
        else:
            tech_stack = self.tech_stack

        repository_url: None | str | Unset
        if isinstance(self.repository_url, Unset):
            repository_url = UNSET
        else:
            repository_url = self.repository_url

        website_url: None | str | Unset
        if isinstance(self.website_url, Unset):
            website_url = UNSET
        else:
            website_url = self.website_url

        team_size = self.team_size

        hiring = self.hiring

        is_archived = self.is_archived

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "slug": slug,
                "description": description,
                "stage": stage,
                "visibility": visibility,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if tagline is not UNSET:
            field_dict["tagline"] = tagline
        if tech_stack is not UNSET:
            field_dict["tech_stack"] = tech_stack
        if repository_url is not UNSET:
            field_dict["repository_url"] = repository_url
        if website_url is not UNSET:
            field_dict["website_url"] = website_url
        if team_size is not UNSET:
            field_dict["team_size"] = team_size
        if hiring is not UNSET:
            field_dict["hiring"] = hiring
        if is_archived is not UNSET:
            field_dict["is_archived"] = is_archived

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        title = d.pop("title")

        slug = d.pop("slug")

        description = d.pop("description")

        stage = d.pop("stage")

        visibility = d.pop("visibility")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        def _parse_tagline(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tagline = _parse_tagline(d.pop("tagline", UNSET))

        def _parse_tech_stack(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tech_stack = _parse_tech_stack(d.pop("tech_stack", UNSET))

        def _parse_repository_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        repository_url = _parse_repository_url(d.pop("repository_url", UNSET))

        def _parse_website_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        website_url = _parse_website_url(d.pop("website_url", UNSET))

        team_size = d.pop("team_size", UNSET)

        hiring = d.pop("hiring", UNSET)

        is_archived = d.pop("is_archived", UNSET)

        exported_project = cls(
            id=id,
            title=title,
            slug=slug,
            description=description,
            stage=stage,
            visibility=visibility,
            created_at=created_at,
            updated_at=updated_at,
            tagline=tagline,
            tech_stack=tech_stack,
            repository_url=repository_url,
            website_url=website_url,
            team_size=team_size,
            hiring=hiring,
            is_archived=is_archived,
        )

        exported_project.additional_properties = d
        return exported_project

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
