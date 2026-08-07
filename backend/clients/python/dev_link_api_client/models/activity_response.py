from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.activity_type import ActivityType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.activity_actor import ActivityActor
    from ..models.activity_response_metadata import ActivityResponseMetadata


T = TypeVar("T", bound="ActivityResponse")


@_attrs_define
class ActivityResponse:
    """
    Attributes:
        activity_type (ActivityType):
        title (str):
        id (UUID):
        actor_id (UUID):
        created_at (datetime.datetime):
        description (None | str | Unset):
        target_id (None | Unset | UUID):
        target_type (None | str | Unset):
        metadata (ActivityResponseMetadata | Unset):
        icon (None | str | Unset):
        color (None | str | Unset):
        actor (ActivityActor | None | Unset):
    """

    activity_type: ActivityType
    title: str
    id: UUID
    actor_id: UUID
    created_at: datetime.datetime
    description: None | str | Unset = UNSET
    target_id: None | Unset | UUID = UNSET
    target_type: None | str | Unset = UNSET
    metadata: ActivityResponseMetadata | Unset = UNSET
    icon: None | str | Unset = UNSET
    color: None | str | Unset = UNSET
    actor: ActivityActor | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.activity_actor import ActivityActor

        activity_type = self.activity_type.value

        title = self.title

        id = str(self.id)

        actor_id = str(self.actor_id)

        created_at = self.created_at.isoformat()

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

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

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

        actor: dict[str, Any] | None | Unset
        if isinstance(self.actor, Unset):
            actor = UNSET
        elif isinstance(self.actor, ActivityActor):
            actor = self.actor.to_dict()
        else:
            actor = self.actor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "activity_type": activity_type,
                "title": title,
                "id": id,
                "actor_id": actor_id,
                "created_at": created_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if target_id is not UNSET:
            field_dict["target_id"] = target_id
        if target_type is not UNSET:
            field_dict["target_type"] = target_type
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if icon is not UNSET:
            field_dict["icon"] = icon
        if color is not UNSET:
            field_dict["color"] = color
        if actor is not UNSET:
            field_dict["actor"] = actor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.activity_actor import ActivityActor
        from ..models.activity_response_metadata import ActivityResponseMetadata

        d = dict(src_dict)
        activity_type = ActivityType(d.pop("activity_type"))

        title = d.pop("title")

        id = UUID(d.pop("id"))

        actor_id = UUID(d.pop("actor_id"))

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

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

        _metadata = d.pop("metadata", UNSET)
        metadata: ActivityResponseMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ActivityResponseMetadata.from_dict(_metadata)

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

        def _parse_actor(data: object) -> ActivityActor | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                actor_type_0 = ActivityActor.from_dict(data)

                return actor_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ActivityActor | None | Unset, data)

        actor = _parse_actor(d.pop("actor", UNSET))

        activity_response = cls(
            activity_type=activity_type,
            title=title,
            id=id,
            actor_id=actor_id,
            created_at=created_at,
            description=description,
            target_id=target_id,
            target_type=target_type,
            metadata=metadata,
            icon=icon,
            color=color,
            actor=actor,
        )

        activity_response.additional_properties = d
        return activity_response

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
