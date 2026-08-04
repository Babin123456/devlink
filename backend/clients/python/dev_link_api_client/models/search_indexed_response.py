from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_indexed_result_item import SearchIndexedResultItem


T = TypeVar("T", bound="SearchIndexedResponse")


@_attrs_define
class SearchIndexedResponse:
    """
    Attributes:
        query (str):
        total_results (int):
        execution_time_ms (float):
        results (list[SearchIndexedResultItem]):
        category (None | str | Unset):
    """

    query: str
    total_results: int
    execution_time_ms: float
    results: list[SearchIndexedResultItem]
    category: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        total_results = self.total_results

        execution_time_ms = self.execution_time_ms

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "total_results": total_results,
                "execution_time_ms": execution_time_ms,
                "results": results,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_indexed_result_item import SearchIndexedResultItem

        d = dict(src_dict)
        query = d.pop("query")

        total_results = d.pop("total_results")

        execution_time_ms = d.pop("execution_time_ms")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = SearchIndexedResultItem.from_dict(results_item_data)

            results.append(results_item)

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        search_indexed_response = cls(
            query=query,
            total_results=total_results,
            execution_time_ms=execution_time_ms,
            results=results,
            category=category,
        )

        search_indexed_response.additional_properties = d
        return search_indexed_response

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
