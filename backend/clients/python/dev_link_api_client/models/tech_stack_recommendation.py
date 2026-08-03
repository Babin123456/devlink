from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TechStackRecommendation")


@_attrs_define
class TechStackRecommendation:
    """A single recommended technology with justification.

    Attributes:
        name (str): Name of the recommended technology.
        category (str): Category: frontend, backend, database, cache, devops, etc.
        reason (str): Why this technology is recommended for the given project idea.
        confidence (float | Unset): Confidence score for this recommendation (0.0 to 1.0). Default: 0.5.
    """

    name: str
    category: str
    reason: str
    confidence: float | Unset = 0.5
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        category = self.category

        reason = self.reason

        confidence = self.confidence

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "category": category,
                "reason": reason,
            }
        )
        if confidence is not UNSET:
            field_dict["confidence"] = confidence

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        category = d.pop("category")

        reason = d.pop("reason")

        confidence = d.pop("confidence", UNSET)

        tech_stack_recommendation = cls(
            name=name,
            category=category,
            reason=reason,
            confidence=confidence,
        )

        tech_stack_recommendation.additional_properties = d
        return tech_stack_recommendation

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
