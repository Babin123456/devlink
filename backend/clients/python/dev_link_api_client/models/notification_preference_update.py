from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationPreferenceUpdate")


@_attrs_define
class NotificationPreferenceUpdate:
    """
    Attributes:
        email_enabled (bool | None | Unset):
        websocket_enabled (bool | None | Unset):
        database_enabled (bool | None | Unset):
        project_updates (bool | None | Unset):
        invitations (bool | None | Unset):
        role_changes (bool | None | Unset):
        marketing_emails (bool | None | Unset):
        system_alerts (bool | None | Unset):
    """

    email_enabled: bool | None | Unset = UNSET
    websocket_enabled: bool | None | Unset = UNSET
    database_enabled: bool | None | Unset = UNSET
    project_updates: bool | None | Unset = UNSET
    invitations: bool | None | Unset = UNSET
    role_changes: bool | None | Unset = UNSET
    marketing_emails: bool | None | Unset = UNSET
    system_alerts: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email_enabled: bool | None | Unset
        if isinstance(self.email_enabled, Unset):
            email_enabled = UNSET
        else:
            email_enabled = self.email_enabled

        websocket_enabled: bool | None | Unset
        if isinstance(self.websocket_enabled, Unset):
            websocket_enabled = UNSET
        else:
            websocket_enabled = self.websocket_enabled

        database_enabled: bool | None | Unset
        if isinstance(self.database_enabled, Unset):
            database_enabled = UNSET
        else:
            database_enabled = self.database_enabled

        project_updates: bool | None | Unset
        if isinstance(self.project_updates, Unset):
            project_updates = UNSET
        else:
            project_updates = self.project_updates

        invitations: bool | None | Unset
        if isinstance(self.invitations, Unset):
            invitations = UNSET
        else:
            invitations = self.invitations

        role_changes: bool | None | Unset
        if isinstance(self.role_changes, Unset):
            role_changes = UNSET
        else:
            role_changes = self.role_changes

        marketing_emails: bool | None | Unset
        if isinstance(self.marketing_emails, Unset):
            marketing_emails = UNSET
        else:
            marketing_emails = self.marketing_emails

        system_alerts: bool | None | Unset
        if isinstance(self.system_alerts, Unset):
            system_alerts = UNSET
        else:
            system_alerts = self.system_alerts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email_enabled is not UNSET:
            field_dict["email_enabled"] = email_enabled
        if websocket_enabled is not UNSET:
            field_dict["websocket_enabled"] = websocket_enabled
        if database_enabled is not UNSET:
            field_dict["database_enabled"] = database_enabled
        if project_updates is not UNSET:
            field_dict["project_updates"] = project_updates
        if invitations is not UNSET:
            field_dict["invitations"] = invitations
        if role_changes is not UNSET:
            field_dict["role_changes"] = role_changes
        if marketing_emails is not UNSET:
            field_dict["marketing_emails"] = marketing_emails
        if system_alerts is not UNSET:
            field_dict["system_alerts"] = system_alerts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_email_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        email_enabled = _parse_email_enabled(d.pop("email_enabled", UNSET))

        def _parse_websocket_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        websocket_enabled = _parse_websocket_enabled(d.pop("websocket_enabled", UNSET))

        def _parse_database_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        database_enabled = _parse_database_enabled(d.pop("database_enabled", UNSET))

        def _parse_project_updates(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        project_updates = _parse_project_updates(d.pop("project_updates", UNSET))

        def _parse_invitations(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        invitations = _parse_invitations(d.pop("invitations", UNSET))

        def _parse_role_changes(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        role_changes = _parse_role_changes(d.pop("role_changes", UNSET))

        def _parse_marketing_emails(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        marketing_emails = _parse_marketing_emails(d.pop("marketing_emails", UNSET))

        def _parse_system_alerts(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        system_alerts = _parse_system_alerts(d.pop("system_alerts", UNSET))

        notification_preference_update = cls(
            email_enabled=email_enabled,
            websocket_enabled=websocket_enabled,
            database_enabled=database_enabled,
            project_updates=project_updates,
            invitations=invitations,
            role_changes=role_changes,
            marketing_emails=marketing_emails,
            system_alerts=system_alerts,
        )

        notification_preference_update.additional_properties = d
        return notification_preference_update

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
