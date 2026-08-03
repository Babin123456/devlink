from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dau_metric import DAUMetric


T = TypeVar("T", bound="ActiveUsersOverview")


@_attrs_define
class ActiveUsersOverview:
    """
    Attributes:
        dau (int): Daily Active Users (last 24 hours)
        wau (int): Weekly Active Users (last 7 days)
        mau (int): Monthly Active Users (last 30 days)
        daily_trend (list[DAUMetric] | Unset): Daily active users time series breakdown
    """

    dau: int
    wau: int
    mau: int
    daily_trend: list[DAUMetric] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dau = self.dau

        wau = self.wau

        mau = self.mau

        daily_trend: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.daily_trend, Unset):
            daily_trend = []
            for daily_trend_item_data in self.daily_trend:
                daily_trend_item = daily_trend_item_data.to_dict()
                daily_trend.append(daily_trend_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dau": dau,
                "wau": wau,
                "mau": mau,
            }
        )
        if daily_trend is not UNSET:
            field_dict["daily_trend"] = daily_trend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dau_metric import DAUMetric

        d = dict(src_dict)
        dau = d.pop("dau")

        wau = d.pop("wau")

        mau = d.pop("mau")

        _daily_trend = d.pop("daily_trend", UNSET)
        daily_trend: list[DAUMetric] | Unset = UNSET
        if _daily_trend is not UNSET:
            daily_trend = []
            for daily_trend_item_data in _daily_trend:
                daily_trend_item = DAUMetric.from_dict(daily_trend_item_data)

                daily_trend.append(daily_trend_item)

        active_users_overview = cls(
            dau=dau,
            wau=wau,
            mau=mau,
            daily_trend=daily_trend,
        )

        active_users_overview.additional_properties = d
        return active_users_overview

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
