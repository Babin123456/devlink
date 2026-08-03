from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.daily_view_metric import DailyViewMetric


T = TypeVar("T", bound="ProjectAnalyticsResponse")


@_attrs_define
class ProjectAnalyticsResponse:
    """
    Attributes:
        project_id (UUID):
        total_views (int): Total page views accumulated by the project
        unique_viewers (int): Total distinct viewers recorded
        daily_views (list[DailyViewMetric] | Unset): Daily breakdown of page views for the specified timeframe
    """

    project_id: UUID
    total_views: int
    unique_viewers: int
    daily_views: list[DailyViewMetric] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        total_views = self.total_views

        unique_viewers = self.unique_viewers

        daily_views: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.daily_views, Unset):
            daily_views = []
            for daily_views_item_data in self.daily_views:
                daily_views_item = daily_views_item_data.to_dict()
                daily_views.append(daily_views_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
                "total_views": total_views,
                "unique_viewers": unique_viewers,
            }
        )
        if daily_views is not UNSET:
            field_dict["daily_views"] = daily_views

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.daily_view_metric import DailyViewMetric

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        total_views = d.pop("total_views")

        unique_viewers = d.pop("unique_viewers")

        _daily_views = d.pop("daily_views", UNSET)
        daily_views: list[DailyViewMetric] | Unset = UNSET
        if _daily_views is not UNSET:
            daily_views = []
            for daily_views_item_data in _daily_views:
                daily_views_item = DailyViewMetric.from_dict(daily_views_item_data)

                daily_views.append(daily_views_item)

        project_analytics_response = cls(
            project_id=project_id,
            total_views=total_views,
            unique_viewers=unique_viewers,
            daily_views=daily_views,
        )

        project_analytics_response.additional_properties = d
        return project_analytics_response

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
