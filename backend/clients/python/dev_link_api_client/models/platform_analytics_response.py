from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.active_users_overview import ActiveUsersOverview
    from ..models.conversion_metric import ConversionMetric
    from ..models.project_growth_metric import ProjectGrowthMetric
    from ..models.retention_metric import RetentionMetric


T = TypeVar("T", bound="PlatformAnalyticsResponse")


@_attrs_define
class PlatformAnalyticsResponse:
    """
    Attributes:
        timeframe_days (int): Analysis window length in days
        active_users (ActiveUsersOverview):
        retention (RetentionMetric):
        conversion (ConversionMetric):
        project_growth (ProjectGrowthMetric):
    """

    timeframe_days: int
    active_users: ActiveUsersOverview
    retention: RetentionMetric
    conversion: ConversionMetric
    project_growth: ProjectGrowthMetric
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timeframe_days = self.timeframe_days

        active_users = self.active_users.to_dict()

        retention = self.retention.to_dict()

        conversion = self.conversion.to_dict()

        project_growth = self.project_growth.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timeframe_days": timeframe_days,
                "active_users": active_users,
                "retention": retention,
                "conversion": conversion,
                "project_growth": project_growth,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.active_users_overview import ActiveUsersOverview
        from ..models.conversion_metric import ConversionMetric
        from ..models.project_growth_metric import ProjectGrowthMetric
        from ..models.retention_metric import RetentionMetric

        d = dict(src_dict)
        timeframe_days = d.pop("timeframe_days")

        active_users = ActiveUsersOverview.from_dict(d.pop("active_users"))

        retention = RetentionMetric.from_dict(d.pop("retention"))

        conversion = ConversionMetric.from_dict(d.pop("conversion"))

        project_growth = ProjectGrowthMetric.from_dict(d.pop("project_growth"))

        platform_analytics_response = cls(
            timeframe_days=timeframe_days,
            active_users=active_users,
            retention=retention,
            conversion=conversion,
            project_growth=project_growth,
        )

        platform_analytics_response.additional_properties = d
        return platform_analytics_response

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
