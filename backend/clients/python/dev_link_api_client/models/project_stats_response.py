from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectStatsResponse")


@_attrs_define
class ProjectStatsResponse:
    """
    Attributes:
        project_id (UUID):
        views (int):
        applicants (int):
        accepted_members (int):
        bookmark_count (int):
    """

    project_id: UUID
    views: int
    applicants: int
    accepted_members: int
    bookmark_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        views = self.views

        applicants = self.applicants

        accepted_members = self.accepted_members

        bookmark_count = self.bookmark_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "views": views,
                "applicants": applicants,
                "accepted_members": accepted_members,
                "bookmark_count": bookmark_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        views = d.pop("views")

        applicants = d.pop("applicants")

        accepted_members = d.pop("accepted_members")

        bookmark_count = d.pop("bookmark_count")

        project_stats_response = cls(
            project_id=project_id,
            views=views,
            applicants=applicants,
            accepted_members=accepted_members,
            bookmark_count=bookmark_count,
        )

        project_stats_response.additional_properties = d
        return project_stats_response

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
