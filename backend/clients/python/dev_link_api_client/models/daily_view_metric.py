from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DailyViewMetric")


@_attrs_define
class DailyViewMetric:
    """
    Attributes:
        date (str): Date string in YYYY-MM-DD format
        views (int): Total views for the day
        unique_views (int): Unique viewers for the day
    """

    date: str
    views: int
    unique_views: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        views = self.views

        unique_views = self.unique_views

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "views": views,
                "unique_views": unique_views,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        views = d.pop("views")

        unique_views = d.pop("unique_views")

        daily_view_metric = cls(
            date=date,
            views=views,
            unique_views=unique_views,
        )

        daily_view_metric.additional_properties = d
        return daily_view_metric

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
