from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserStats")


@_attrs_define
class UserStats:
    """
    Attributes:
        projects (int | Unset):  Default: 0.
        followers (int | Unset):  Default: 0.
        following (int | Unset):  Default: 0.
        applications (int | Unset):  Default: 0.
        accepted (int | Unset):  Default: 0.
    """

    projects: int | Unset = 0
    followers: int | Unset = 0
    following: int | Unset = 0
    applications: int | Unset = 0
    accepted: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        projects = self.projects

        followers = self.followers

        following = self.following

        applications = self.applications

        accepted = self.accepted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if projects is not UNSET:
            field_dict["projects"] = projects
        if followers is not UNSET:
            field_dict["followers"] = followers
        if following is not UNSET:
            field_dict["following"] = following
        if applications is not UNSET:
            field_dict["applications"] = applications
        if accepted is not UNSET:
            field_dict["accepted"] = accepted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        projects = d.pop("projects", UNSET)

        followers = d.pop("followers", UNSET)

        following = d.pop("following", UNSET)

        applications = d.pop("applications", UNSET)

        accepted = d.pop("accepted", UNSET)

        user_stats = cls(
            projects=projects,
            followers=followers,
            following=following,
            applications=applications,
            accepted=accepted,
        )

        user_stats.additional_properties = d
        return user_stats

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
