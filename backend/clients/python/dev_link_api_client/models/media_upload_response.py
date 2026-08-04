from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MediaUploadResponse")


@_attrs_define
class MediaUploadResponse:
    """
    Attributes:
        hash_ (str):
        url (str):
        thumbnail_url (str):
        reused (bool):
    """

    hash_: str
    url: str
    thumbnail_url: str
    reused: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hash_ = self.hash_

        url = self.url

        thumbnail_url = self.thumbnail_url

        reused = self.reused

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hash": hash_,
                "url": url,
                "thumbnail_url": thumbnail_url,
                "reused": reused,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hash_ = d.pop("hash")

        url = d.pop("url")

        thumbnail_url = d.pop("thumbnail_url")

        reused = d.pop("reused")

        media_upload_response = cls(
            hash_=hash_,
            url=url,
            thumbnail_url=thumbnail_url,
            reused=reused,
        )

        media_upload_response.additional_properties = d
        return media_upload_response

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
