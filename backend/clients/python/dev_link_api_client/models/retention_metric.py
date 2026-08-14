from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RetentionMetric")


@_attrs_define
class RetentionMetric:
    """
    Attributes:
        retention_7d_pct (float): Percentage of users registered >7 days ago who were active in last 7 days
        retention_30d_pct (float): Percentage of users registered >30 days ago who were active in last 30 days
        retained_7d_users (int): Count of retained users over 7 days
        eligible_7d_users (int): Count of users eligible for 7-day retention
        retained_30d_users (int): Count of retained users over 30 days
        eligible_30d_users (int): Count of users eligible for 30-day retention
    """

    retention_7d_pct: float
    retention_30d_pct: float
    retained_7d_users: int
    eligible_7d_users: int
    retained_30d_users: int
    eligible_30d_users: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        retention_7d_pct = self.retention_7d_pct

        retention_30d_pct = self.retention_30d_pct

        retained_7d_users = self.retained_7d_users

        eligible_7d_users = self.eligible_7d_users

        retained_30d_users = self.retained_30d_users

        eligible_30d_users = self.eligible_30d_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "retention_7d_pct": retention_7d_pct,
                "retention_30d_pct": retention_30d_pct,
                "retained_7d_users": retained_7d_users,
                "eligible_7d_users": eligible_7d_users,
                "retained_30d_users": retained_30d_users,
                "eligible_30d_users": eligible_30d_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        retention_7d_pct = d.pop("retention_7d_pct")

        retention_30d_pct = d.pop("retention_30d_pct")

        retained_7d_users = d.pop("retained_7d_users")

        eligible_7d_users = d.pop("eligible_7d_users")

        retained_30d_users = d.pop("retained_30d_users")

        eligible_30d_users = d.pop("eligible_30d_users")

        retention_metric = cls(
            retention_7d_pct=retention_7d_pct,
            retention_30d_pct=retention_30d_pct,
            retained_7d_users=retained_7d_users,
            eligible_7d_users=eligible_7d_users,
            retained_30d_users=retained_30d_users,
            eligible_30d_users=eligible_30d_users,
        )

        retention_metric.additional_properties = d
        return retention_metric

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
