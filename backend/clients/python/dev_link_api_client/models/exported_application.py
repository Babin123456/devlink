from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportedApplication")


@_attrs_define
class ExportedApplication:
    """
    Attributes:
        id (UUID):
        project_id (UUID):
        status (str):
        created_at (datetime.datetime):
        message (None | str | Unset):
        portfolio_url (None | str | Unset):
        github_url (None | str | Unset):
    """

    id: UUID
    project_id: UUID
    status: str
    created_at: datetime.datetime
    message: None | str | Unset = UNSET
    portfolio_url: None | str | Unset = UNSET
    github_url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        status = self.status

        created_at = self.created_at.isoformat()

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        portfolio_url: None | str | Unset
        if isinstance(self.portfolio_url, Unset):
            portfolio_url = UNSET
        else:
            portfolio_url = self.portfolio_url

        github_url: None | str | Unset
        if isinstance(self.github_url, Unset):
            github_url = UNSET
        else:
            github_url = self.github_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "status": status,
                "created_at": created_at,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if portfolio_url is not UNSET:
            field_dict["portfolio_url"] = portfolio_url
        if github_url is not UNSET:
            field_dict["github_url"] = github_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        project_id = UUID(d.pop("project_id"))

        status = d.pop("status")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_portfolio_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        portfolio_url = _parse_portfolio_url(d.pop("portfolio_url", UNSET))

        def _parse_github_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        github_url = _parse_github_url(d.pop("github_url", UNSET))

        exported_application = cls(
            id=id,
            project_id=project_id,
            status=status,
            created_at=created_at,
            message=message,
            portfolio_url=portfolio_url,
            github_url=github_url,
        )

        exported_application.additional_properties = d
        return exported_application

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
