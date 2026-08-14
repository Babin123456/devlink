from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchBenchmarkReport")


@_attrs_define
class SearchBenchmarkReport:
    """
    Attributes:
        query (str):
        iterations (int):
        naive_sql_avg_ms (float):
        inverted_index_avg_ms (float):
        latency_reduction_percent (float):
        speedup_factor (float):
        status (str):
    """

    query: str
    iterations: int
    naive_sql_avg_ms: float
    inverted_index_avg_ms: float
    latency_reduction_percent: float
    speedup_factor: float
    status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        iterations = self.iterations

        naive_sql_avg_ms = self.naive_sql_avg_ms

        inverted_index_avg_ms = self.inverted_index_avg_ms

        latency_reduction_percent = self.latency_reduction_percent

        speedup_factor = self.speedup_factor

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "iterations": iterations,
                "naive_sql_avg_ms": naive_sql_avg_ms,
                "inverted_index_avg_ms": inverted_index_avg_ms,
                "latency_reduction_percent": latency_reduction_percent,
                "speedup_factor": speedup_factor,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        iterations = d.pop("iterations")

        naive_sql_avg_ms = d.pop("naive_sql_avg_ms")

        inverted_index_avg_ms = d.pop("inverted_index_avg_ms")

        latency_reduction_percent = d.pop("latency_reduction_percent")

        speedup_factor = d.pop("speedup_factor")

        status = d.pop("status")

        search_benchmark_report = cls(
            query=query,
            iterations=iterations,
            naive_sql_avg_ms=naive_sql_avg_ms,
            inverted_index_avg_ms=inverted_index_avg_ms,
            latency_reduction_percent=latency_reduction_percent,
            speedup_factor=speedup_factor,
            status=status,
        )

        search_benchmark_report.additional_properties = d
        return search_benchmark_report

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
