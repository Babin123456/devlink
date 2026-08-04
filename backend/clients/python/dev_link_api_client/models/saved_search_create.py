from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_search_filters import ProjectSearchFilters


T = TypeVar("T", bound="SavedSearchCreate")


@_attrs_define
class SavedSearchCreate:
    """
    Attributes:
        name (str):
        filters (ProjectSearchFilters): Represents the filterable fields on a project search.
    """

    name: str
    filters: ProjectSearchFilters
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        filters = self.filters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "filters": filters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_search_filters import ProjectSearchFilters

        d = dict(src_dict)
        name = d.pop("name")

        filters = ProjectSearchFilters.from_dict(d.pop("filters"))

        saved_search_create = cls(
            name=name,
            filters=filters,
        )

        saved_search_create.additional_properties = d
        return saved_search_create

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
