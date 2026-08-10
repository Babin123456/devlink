from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SimilarProjectWarning")


@_attrs_define
class SimilarProjectWarning:
    """
    Attributes:
        id (UUID):
        title (str):
        slug (str):
        title_similarity (float):
        description_similarity (float):
    """

    id: UUID
    title: str
    slug: str
    title_similarity: float
    description_similarity: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        title = self.title

        slug = self.slug

        title_similarity = self.title_similarity

        description_similarity = self.description_similarity

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "slug": slug,
                "title_similarity": title_similarity,
                "description_similarity": description_similarity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        title = d.pop("title")

        slug = d.pop("slug")

        title_similarity = d.pop("title_similarity")

        description_similarity = d.pop("description_similarity")

        similar_project_warning = cls(
            id=id,
            title=title,
            slug=slug,
            title_similarity=title_similarity,
            description_similarity=description_similarity,
        )

        similar_project_warning.additional_properties = d
        return similar_project_warning

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
