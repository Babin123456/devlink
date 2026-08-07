from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.saved_search_response_filters import SavedSearchResponseFilters


T = TypeVar("T", bound="SavedSearchResponse")


@_attrs_define
class SavedSearchResponse:
    """
    Attributes:
        id (UUID):
        user_id (UUID):
        name (str):
        filters (SavedSearchResponseFilters):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: UUID
    user_id: UUID
    name: str
    filters: SavedSearchResponseFilters
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = str(self.user_id)

        name = self.name

        filters = self.filters.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "name": name,
                "filters": filters,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.saved_search_response_filters import SavedSearchResponseFilters

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        user_id = UUID(d.pop("user_id"))

        name = d.pop("name")

        filters = SavedSearchResponseFilters.from_dict(d.pop("filters"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))

        saved_search_response = cls(
            id=id,
            user_id=user_id,
            name=name,
            filters=filters,
            created_at=created_at,
            updated_at=updated_at,
        )

        saved_search_response.additional_properties = d
        return saved_search_response

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
