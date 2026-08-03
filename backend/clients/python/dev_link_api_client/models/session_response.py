from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionResponse")


@_attrs_define
class SessionResponse:
    """
    Attributes:
        id (UUID):
        is_revoked (bool):
        created_at (datetime.datetime):
        expires_at (datetime.datetime):
        device_name (None | str | Unset):
        device_type (None | str | Unset):
        browser (None | str | Unset):
        operating_system (None | str | Unset):
        ip_address (None | str | Unset):
        user_agent (None | str | Unset):
        last_used_at (datetime.datetime | None | Unset):
        is_current (bool | Unset): Indicates whether this is the session used for the current request Default: False.
    """

    id: UUID
    is_revoked: bool
    created_at: datetime.datetime
    expires_at: datetime.datetime
    device_name: None | str | Unset = UNSET
    device_type: None | str | Unset = UNSET
    browser: None | str | Unset = UNSET
    operating_system: None | str | Unset = UNSET
    ip_address: None | str | Unset = UNSET
    user_agent: None | str | Unset = UNSET
    last_used_at: datetime.datetime | None | Unset = UNSET
    is_current: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        is_revoked = self.is_revoked

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        device_name: None | str | Unset
        if isinstance(self.device_name, Unset):
            device_name = UNSET
        else:
            device_name = self.device_name

        device_type: None | str | Unset
        if isinstance(self.device_type, Unset):
            device_type = UNSET
        else:
            device_type = self.device_type

        browser: None | str | Unset
        if isinstance(self.browser, Unset):
            browser = UNSET
        else:
            browser = self.browser

        operating_system: None | str | Unset
        if isinstance(self.operating_system, Unset):
            operating_system = UNSET
        else:
            operating_system = self.operating_system

        ip_address: None | str | Unset
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        user_agent: None | str | Unset
        if isinstance(self.user_agent, Unset):
            user_agent = UNSET
        else:
            user_agent = self.user_agent

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        elif isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        is_current = self.is_current

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "is_revoked": is_revoked,
                "created_at": created_at,
                "expires_at": expires_at,
            }
        )
        if device_name is not UNSET:
            field_dict["device_name"] = device_name
        if device_type is not UNSET:
            field_dict["device_type"] = device_type
        if browser is not UNSET:
            field_dict["browser"] = browser
        if operating_system is not UNSET:
            field_dict["operating_system"] = operating_system
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if user_agent is not UNSET:
            field_dict["user_agent"] = user_agent
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at
        if is_current is not UNSET:
            field_dict["is_current"] = is_current

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        is_revoked = d.pop("is_revoked")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        expires_at = datetime.datetime.fromisoformat(d.pop("expires_at"))

        def _parse_device_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        device_name = _parse_device_name(d.pop("device_name", UNSET))

        def _parse_device_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        device_type = _parse_device_type(d.pop("device_type", UNSET))

        def _parse_browser(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        browser = _parse_browser(d.pop("browser", UNSET))

        def _parse_operating_system(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        operating_system = _parse_operating_system(d.pop("operating_system", UNSET))

        def _parse_ip_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        def _parse_user_agent(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_agent = _parse_user_agent(d.pop("user_agent", UNSET))

        def _parse_last_used_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = datetime.datetime.fromisoformat(data)

                return last_used_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        is_current = d.pop("is_current", UNSET)

        session_response = cls(
            id=id,
            is_revoked=is_revoked,
            created_at=created_at,
            expires_at=expires_at,
            device_name=device_name,
            device_type=device_type,
            browser=browser,
            operating_system=operating_system,
            ip_address=ip_address,
            user_agent=user_agent,
            last_used_at=last_used_at,
            is_current=is_current,
        )

        session_response.additional_properties = d
        return session_response

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
