from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecommendationProject")


@_attrs_define
class RecommendationProject:
    """Simplified project representation for recommendation results.
    Includes key fields for display without heavy nesting.

        Attributes:
            id (UUID):
            owner_id (UUID):
            title (str):
            slug (str):
            description (str):
            stage (str):
            team_size (int):
            max_team_size (int):
            hiring (bool):
            stars (int):
            views (int):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            tagline (None | str | Unset):
            tech_stack (None | str | Unset):
            repository_url (None | str | Unset):
            logo_url (None | str | Unset):
            banner_url (None | str | Unset):
    """

    id: UUID
    owner_id: UUID
    title: str
    slug: str
    description: str
    stage: str
    team_size: int
    max_team_size: int
    hiring: bool
    stars: int
    views: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tagline: None | str | Unset = UNSET
    tech_stack: None | str | Unset = UNSET
    repository_url: None | str | Unset = UNSET
    logo_url: None | str | Unset = UNSET
    banner_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        owner_id = str(self.owner_id)

        title = self.title

        slug = self.slug

        description = self.description

        stage = self.stage

        team_size = self.team_size

        max_team_size = self.max_team_size

        hiring = self.hiring

        stars = self.stars

        views = self.views

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

        logo_url: None | str | Unset
        if isinstance(self.logo_url, Unset):
            logo_url = UNSET
        else:
            logo_url = self.logo_url

        banner_url: None | str | Unset
        if isinstance(self.banner_url, Unset):
            banner_url = UNSET
        else:
            banner_url = self.banner_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "owner_id": owner_id,
                "title": title,
                "slug": slug,
                "description": description,
                "stage": stage,
                "team_size": team_size,
                "max_team_size": max_team_size,
                "hiring": hiring,
                "stars": stars,
                "views": views,
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
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url
        if banner_url is not UNSET:
            field_dict["banner_url"] = banner_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        owner_id = UUID(d.pop("owner_id"))

        title = d.pop("title")

        slug = d.pop("slug")

        description = d.pop("description")

        stage = d.pop("stage")

        team_size = d.pop("team_size")

        max_team_size = d.pop("max_team_size")

        hiring = d.pop("hiring")

        stars = d.pop("stars")

        views = d.pop("views")

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

        def _parse_logo_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo_url = _parse_logo_url(d.pop("logo_url", UNSET))

        def _parse_banner_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        banner_url = _parse_banner_url(d.pop("banner_url", UNSET))

        recommendation_project = cls(
            id=id,
            owner_id=owner_id,
            title=title,
            slug=slug,
            description=description,
            stage=stage,
            team_size=team_size,
            max_team_size=max_team_size,
            hiring=hiring,
            stars=stars,
            views=views,
            created_at=created_at,
            updated_at=updated_at,
            tagline=tagline,
            tech_stack=tech_stack,
            repository_url=repository_url,
            logo_url=logo_url,
            banner_url=banner_url,
        )

        recommendation_project.additional_properties = d
        return recommendation_project

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
