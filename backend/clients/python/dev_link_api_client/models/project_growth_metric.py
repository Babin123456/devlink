from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.daily_project_metric import DailyProjectMetric


T = TypeVar("T", bound="ProjectGrowthMetric")


@_attrs_define
class ProjectGrowthMetric:
    """
    Attributes:
        total_projects (int): Total projects count in database
        new_projects_period (int): New projects created in the specified period
        growth_rate_pct (float): Percentage growth in projects over the period
        daily_growth (list[DailyProjectMetric] | Unset): Daily breakdown of project creation over time
    """

    total_projects: int
    new_projects_period: int
    growth_rate_pct: float
    daily_growth: list[DailyProjectMetric] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_projects = self.total_projects

        new_projects_period = self.new_projects_period

        growth_rate_pct = self.growth_rate_pct

        daily_growth: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.daily_growth, Unset):
            daily_growth = []
            for daily_growth_item_data in self.daily_growth:
                daily_growth_item = daily_growth_item_data.to_dict()
                daily_growth.append(daily_growth_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_projects": total_projects,
                "new_projects_period": new_projects_period,
                "growth_rate_pct": growth_rate_pct,
            }
        )
        if daily_growth is not UNSET:
            field_dict["daily_growth"] = daily_growth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_project_metric import DailyProjectMetric

        d = dict(src_dict)
        total_projects = d.pop("total_projects")

        new_projects_period = d.pop("new_projects_period")

        growth_rate_pct = d.pop("growth_rate_pct")

        _daily_growth = d.pop("daily_growth", UNSET)
        daily_growth: list[DailyProjectMetric] | Unset = UNSET
        if _daily_growth is not UNSET:
            daily_growth = []
            for daily_growth_item_data in _daily_growth:
                daily_growth_item = DailyProjectMetric.from_dict(daily_growth_item_data)

                daily_growth.append(daily_growth_item)

        project_growth_metric = cls(
            total_projects=total_projects,
            new_projects_period=new_projects_period,
            growth_rate_pct=growth_rate_pct,
            daily_growth=daily_growth,
        )

        project_growth_metric.additional_properties = d
        return project_growth_metric

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
