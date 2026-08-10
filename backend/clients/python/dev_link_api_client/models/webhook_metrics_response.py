from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WebhookMetricsResponse")


@_attrs_define
class WebhookMetricsResponse:
    """
    Attributes:
        total_deliveries (int):
        successful_deliveries (int):
        failed_deliveries (int):
        pending_deliveries (int):
        dlq_count (int):
        replayed_count (int):
        delivery_success_rate (float):
    """

    total_deliveries: int
    successful_deliveries: int
    failed_deliveries: int
    pending_deliveries: int
    dlq_count: int
    replayed_count: int
    delivery_success_rate: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_deliveries = self.total_deliveries

        successful_deliveries = self.successful_deliveries

        failed_deliveries = self.failed_deliveries

        pending_deliveries = self.pending_deliveries

        dlq_count = self.dlq_count

        replayed_count = self.replayed_count

        delivery_success_rate = self.delivery_success_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_deliveries": total_deliveries,
                "successful_deliveries": successful_deliveries,
                "failed_deliveries": failed_deliveries,
                "pending_deliveries": pending_deliveries,
                "dlq_count": dlq_count,
                "replayed_count": replayed_count,
                "delivery_success_rate": delivery_success_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_deliveries = d.pop("total_deliveries")

        successful_deliveries = d.pop("successful_deliveries")

        failed_deliveries = d.pop("failed_deliveries")

        pending_deliveries = d.pop("pending_deliveries")

        dlq_count = d.pop("dlq_count")

        replayed_count = d.pop("replayed_count")

        delivery_success_rate = d.pop("delivery_success_rate")

        webhook_metrics_response = cls(
            total_deliveries=total_deliveries,
            successful_deliveries=successful_deliveries,
            failed_deliveries=failed_deliveries,
            pending_deliveries=pending_deliveries,
            dlq_count=dlq_count,
            replayed_count=replayed_count,
            delivery_success_rate=delivery_success_rate,
        )

        webhook_metrics_response.additional_properties = d
        return webhook_metrics_response

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
