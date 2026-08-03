from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recommended_builder import RecommendedBuilder


T = TypeVar("T", bound="RecommendationResponse")


@_attrs_define
class RecommendationResponse:
    """Ranked recommendation list returned by the API.

    Attributes:
        query_context (str): What the recommendations were generated for.
        total (int):
        limit (int):
        results (list[RecommendedBuilder]):
    """

    query_context: str
    total: int
    limit: int
    results: list[RecommendedBuilder]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query_context = self.query_context

        total = self.total

        limit = self.limit

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query_context": query_context,
                "total": total,
                "limit": limit,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recommended_builder import RecommendedBuilder

        d = dict(src_dict)
        query_context = d.pop("query_context")

        total = d.pop("total")

        limit = d.pop("limit")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = RecommendedBuilder.from_dict(results_item_data)

            results.append(results_item)

        recommendation_response = cls(
            query_context=query_context,
            total=total,
            limit=limit,
            results=results,
        )

        recommendation_response.additional_properties = d
        return recommendation_response

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
