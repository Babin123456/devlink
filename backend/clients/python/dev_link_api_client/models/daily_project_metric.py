from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DailyProjectMetric")


@_attrs_define
class DailyProjectMetric:
    """
    Attributes:
        date (str): Date string in YYYY-MM-DD format
        new_projects (int): New projects created on this date
        cumulative_projects (int): Cumulative project count up to this date
    """

    date: str
    new_projects: int
    cumulative_projects: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        new_projects = self.new_projects

        cumulative_projects = self.cumulative_projects

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "new_projects": new_projects,
                "cumulative_projects": cumulative_projects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        new_projects = d.pop("new_projects")

        cumulative_projects = d.pop("cumulative_projects")

        daily_project_metric = cls(
            date=date,
            new_projects=new_projects,
            cumulative_projects=cumulative_projects,
        )

        daily_project_metric.additional_properties = d
        return daily_project_metric

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
