from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.quality_metric import QualityMetric

T = TypeVar("T", bound="ImprovementSuggestion")


@_attrs_define
class ImprovementSuggestion:
    """A single actionable improvement suggestion.

    Attributes:
        priority (str): Priority level: 'high', 'medium', or 'low'.
        category (QualityMetric): Individual quality metrics that can be scored.
        title (str): Short title of the suggestion.
        description (str): Detailed explanation of the improvement.
    """

    priority: str
    category: QualityMetric
    title: str
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        priority = self.priority

        category = self.category.value

        title = self.title

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "priority": priority,
                "category": category,
                "title": title,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        priority = d.pop("priority")

        category = QualityMetric(d.pop("category"))

        title = d.pop("title")

        description = d.pop("description")

        improvement_suggestion = cls(
            priority=priority,
            category=category,
            title=title,
            description=description,
        )

        improvement_suggestion.additional_properties = d
        return improvement_suggestion

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
