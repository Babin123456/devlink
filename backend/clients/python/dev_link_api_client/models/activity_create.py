from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.activity_type import ActivityType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.activity_create_meta import ActivityCreateMeta


T = TypeVar("T", bound="ActivityCreate")


@_attrs_define
class ActivityCreate:
    """
    Attributes:
        activity_type (ActivityType):
        title (str):
        actor_id (UUID):
        description (None | str | Unset):
        target_id (None | Unset | UUID):
        target_type (None | str | Unset):
        meta (ActivityCreateMeta | Unset):
        icon (None | str | Unset):
        color (None | str | Unset):
    """

    activity_type: ActivityType
    title: str
    actor_id: UUID
    description: None | str | Unset = UNSET
    target_id: None | Unset | UUID = UNSET
    target_type: None | str | Unset = UNSET
    meta: ActivityCreateMeta | Unset = UNSET
    icon: None | str | Unset = UNSET
    color: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        activity_type = self.activity_type.value

        title = self.title

        actor_id = str(self.actor_id)

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        target_id: None | str | Unset
        if isinstance(self.target_id, Unset):
            target_id = UNSET
        elif isinstance(self.target_id, UUID):
            target_id = str(self.target_id)
        else:
            target_id = self.target_id

        target_type: None | str | Unset
        if isinstance(self.target_type, Unset):
            target_type = UNSET
        else:
            target_type = self.target_type

        meta: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activity_type": activity_type,
                "title": title,
                "actor_id": actor_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if target_id is not UNSET:
            field_dict["target_id"] = target_id
        if target_type is not UNSET:
            field_dict["target_type"] = target_type
        if meta is not UNSET:
            field_dict["meta"] = meta
        if icon is not UNSET:
            field_dict["icon"] = icon
        if color is not UNSET:
            field_dict["color"] = color

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activity_create_meta import ActivityCreateMeta

        d = dict(src_dict)
        activity_type = ActivityType(d.pop("activity_type"))

        title = d.pop("title")

        actor_id = UUID(d.pop("actor_id"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_target_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                target_id_type_0 = UUID(data)

                return target_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        target_id = _parse_target_id(d.pop("target_id", UNSET))

        def _parse_target_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_type = _parse_target_type(d.pop("target_type", UNSET))

        _meta = d.pop("meta", UNSET)
        meta: ActivityCreateMeta | Unset
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = ActivityCreateMeta.from_dict(_meta)

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

        activity_create = cls(
            activity_type=activity_type,
            title=title,
            actor_id=actor_id,
            description=description,
            target_id=target_id,
            target_type=target_type,
            meta=meta,
            icon=icon,
            color=color,
        )

        activity_create.additional_properties = d
        return activity_create

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
