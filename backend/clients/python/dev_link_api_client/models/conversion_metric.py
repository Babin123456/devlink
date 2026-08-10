from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConversionMetric")


@_attrs_define
class ConversionMetric:
    """
    Attributes:
        profile_completion_pct (float): Percentage of registered users with complete profile details
        project_creator_pct (float): Percentage of registered users who created at least 1 project
        application_acceptance_pct (float): Percentage of builder flare applications that were accepted
        user_application_pct (float): Percentage of registered users who submitted at least 1 application
        completed_profiles_count (int): Total completed user profiles
        project_creators_count (int): Total users with at least 1 project
        total_applications_count (int): Total builder flare applications
        accepted_applications_count (int): Total accepted applications
    """

    profile_completion_pct: float
    project_creator_pct: float
    application_acceptance_pct: float
    user_application_pct: float
    completed_profiles_count: int
    project_creators_count: int
    total_applications_count: int
    accepted_applications_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile_completion_pct = self.profile_completion_pct

        project_creator_pct = self.project_creator_pct

        application_acceptance_pct = self.application_acceptance_pct

        user_application_pct = self.user_application_pct

        completed_profiles_count = self.completed_profiles_count

        project_creators_count = self.project_creators_count

        total_applications_count = self.total_applications_count

        accepted_applications_count = self.accepted_applications_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile_completion_pct": profile_completion_pct,
                "project_creator_pct": project_creator_pct,
                "application_acceptance_pct": application_acceptance_pct,
                "user_application_pct": user_application_pct,
                "completed_profiles_count": completed_profiles_count,
                "project_creators_count": project_creators_count,
                "total_applications_count": total_applications_count,
                "accepted_applications_count": accepted_applications_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profile_completion_pct = d.pop("profile_completion_pct")

        project_creator_pct = d.pop("project_creator_pct")

        application_acceptance_pct = d.pop("application_acceptance_pct")

        user_application_pct = d.pop("user_application_pct")

        completed_profiles_count = d.pop("completed_profiles_count")

        project_creators_count = d.pop("project_creators_count")

        total_applications_count = d.pop("total_applications_count")

        accepted_applications_count = d.pop("accepted_applications_count")

        conversion_metric = cls(
            profile_completion_pct=profile_completion_pct,
            project_creator_pct=project_creator_pct,
            application_acceptance_pct=application_acceptance_pct,
            user_application_pct=user_application_pct,
            completed_profiles_count=completed_profiles_count,
            project_creators_count=project_creators_count,
            total_applications_count=total_applications_count,
            accepted_applications_count=accepted_applications_count,
        )

        conversion_metric.additional_properties = d
        return conversion_metric

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
