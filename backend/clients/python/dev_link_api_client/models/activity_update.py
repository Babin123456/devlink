from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.activity_update_meta_type_0 import ActivityUpdateMetaType0


T = TypeVar("T", bound="ActivityUpdate")


@_attrs_define
class ActivityUpdate:
    """
    Attributes:
        title (None | str | Unset):
        description (None | str | Unset):
        icon (None | str | Unset):
        color (None | str | Unset):
        meta (ActivityUpdateMetaType0 | None | Unset):
    """

    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    icon: None | str | Unset = UNSET
    color: None | str | Unset = UNSET
    meta: ActivityUpdateMetaType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.activity_update_meta_type_0 import ActivityUpdateMetaType0

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        icon: None | str | Unset
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        color: None | str | Unset
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        meta: dict[str, Any] | None | Unset
        if isinstance(self.meta, Unset):
            meta = UNSET
        elif isinstance(self.meta, ActivityUpdateMetaType0):
            meta = self.meta.to_dict()
        else:
            meta = self.meta

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if icon is not UNSET:
            field_dict["icon"] = icon
        if color is not UNSET:
            field_dict["color"] = color
        if meta is not UNSET:
            field_dict["meta"] = meta

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activity_update_meta_type_0 import ActivityUpdateMetaType0

        d = dict(src_dict)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_icon(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_meta(data: object) -> ActivityUpdateMetaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                meta_type_0 = ActivityUpdateMetaType0.from_dict(data)

                return meta_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActivityUpdateMetaType0 | None | Unset, data)

        meta = _parse_meta(d.pop("meta", UNSET))

        activity_update = cls(
            title=title,
            description=description,
            icon=icon,
            color=color,
            meta=meta,
        )

        activity_update.additional_properties = d
        return activity_update

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
