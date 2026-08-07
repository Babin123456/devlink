from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flare_status import FlareStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="BuilderFlareUpdate")


@_attrs_define
class BuilderFlareUpdate:
    """
    Attributes:
        title (None | str | Unset):
        description (None | str | Unset):
        role (None | str | Unset):
        location (None | str | Unset):
        commitment (None | str | Unset):
        experience_level (None | str | Unset):
        openings (int | None | Unset):
        status (FlareStatus | None | Unset):
        remote (bool | None | Unset):
    """

    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    role: None | str | Unset = UNSET
    location: None | str | Unset = UNSET
    commitment: None | str | Unset = UNSET
    experience_level: None | str | Unset = UNSET
    openings: int | None | Unset = UNSET
    status: FlareStatus | None | Unset = UNSET
    remote: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        location: None | str | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        else:
            location = self.location

        commitment: None | str | Unset
        if isinstance(self.commitment, Unset):
            commitment = UNSET
        else:
            commitment = self.commitment

        experience_level: None | str | Unset
        if isinstance(self.experience_level, Unset):
            experience_level = UNSET
        else:
            experience_level = self.experience_level

        openings: int | None | Unset
        if isinstance(self.openings, Unset):
            openings = UNSET
        else:
            openings = self.openings

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, FlareStatus):
            status = self.status.value
        else:
            status = self.status

        remote: bool | None | Unset
        if isinstance(self.remote, Unset):
            remote = UNSET
        else:
            remote = self.remote

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if role is not UNSET:
            field_dict["role"] = role
        if location is not UNSET:
            field_dict["location"] = location
        if commitment is not UNSET:
            field_dict["commitment"] = commitment
        if experience_level is not UNSET:
            field_dict["experience_level"] = experience_level
        if openings is not UNSET:
            field_dict["openings"] = openings
        if status is not UNSET:
            field_dict["status"] = status
        if remote is not UNSET:
            field_dict["remote"] = remote

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_location(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_commitment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        commitment = _parse_commitment(d.pop("commitment", UNSET))

        def _parse_experience_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        experience_level = _parse_experience_level(d.pop("experience_level", UNSET))

        def _parse_openings(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        openings = _parse_openings(d.pop("openings", UNSET))

        def _parse_status(data: object) -> FlareStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = FlareStatus(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FlareStatus | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_remote(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        remote = _parse_remote(d.pop("remote", UNSET))

        builder_flare_update = cls(
            title=title,
            description=description,
            role=role,
            location=location,
            commitment=commitment,
            experience_level=experience_level,
            openings=openings,
            status=status,
            remote=remote,
        )

        builder_flare_update.additional_properties = d
        return builder_flare_update

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
