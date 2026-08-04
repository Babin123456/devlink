from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.quality_metric import QualityMetric

T = TypeVar("T", bound="MetricScore")


@_attrs_define
class MetricScore:
    """Score and details for a single quality metric.

    Attributes:
        metric (QualityMetric): Individual quality metrics that can be scored.
        score (float): Score from 0.0 (worst) to 1.0 (best).
        label (str): Human-readable metric name.
        description (str): Explanation of how this score was computed.
        weight (float): Weight of this metric in the overall score.
    """

    metric: QualityMetric
    score: float
    label: str
    description: str
    weight: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric.value

        score = self.score

        label = self.label

        description = self.description

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "score": score,
                "label": label,
                "description": description,
                "weight": weight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metric = QualityMetric(d.pop("metric"))

        score = d.pop("score")

        label = d.pop("label")

        description = d.pop("description")

        weight = d.pop("weight")

        metric_score = cls(
            metric=metric,
            score=score,
            label=label,
            description=description,
            weight=weight,
        )

        metric_score.additional_properties = d
        return metric_score

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
